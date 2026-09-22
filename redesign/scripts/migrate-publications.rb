#!/usr/bin/env ruby
# One-time import of the legacy archive, using only Ruby's standard library.
# This is NOT part of publishing or adding a new paper. Its output directory must
# be empty, so running it later cannot overwrite manually maintained records.
# Usage: ruby redesign/scripts/migrate-publications.rb --output /tmp/paper-import

require 'yaml'
require 'json'
require 'date'
require 'pathname'
require 'fileutils'
require 'optparse'

options = {}
OptionParser.new do |parser|
  parser.banner = 'Usage: migrate-publications.rb --output EMPTY_DIRECTORY'
  parser.on('--output DIRECTORY', 'Empty staging directory for migrated Markdown') { |v| options[:output] = v }
end.parse!
abort 'Supply --output with an empty staging directory; never import over edited files.' unless options[:output]

ROOT = Pathname.new(__dir__).join('../..').expand_path
LEGACY = ROOT.join('content/publications')
OUTPUT = Pathname.new(options[:output]).expand_path
abort "Output directory is not empty: #{OUTPUT}" if OUTPUT.exist? && !OUTPUT.children.empty?
FileUtils.mkdir_p(OUTPUT)

def read_page(path)
  parts = path.read.split(/^---\s*$\n?/, 3)
  raise "Missing YAML front matter: #{path}" unless parts.length == 3
  [YAML.safe_load(parts[1], permitted_classes: [Date, Time], aliases: false), parts[2].strip]
end

def slugify(text)
  text.downcase.gsub(/[^a-z0-9]+/, '-').gsub(/\A-|-\z/, '')
end

VENUES = {
  'NSDI' => 'USENIX NSDI', 'ATC' => 'USENIX ATC', 'Security' => 'USENIX Security',
  'CCS' => 'ACM CCS', 'CoNEXT' => 'ACM CoNEXT', 'SIGCOMM' => 'ACM SIGCOMM',
  'SIGMOD' => 'ACM SIGMOD', 'ISSTA' => 'ACM ISSTA', 'WWW' => 'The Web Conference',
  'S&P' => 'IEEE S&P', 'NDSS' => 'NDSS', 'INFOCOM' => 'IEEE INFOCOM',
  'IWQoS' => 'IEEE/ACM IWQoS', 'ICNP' => 'IEEE ICNP', 'TIFS' => 'IEEE TIFS',
  'TDSC' => 'IEEE TDSC', 'TPDS' => 'IEEE TPDS'
}.freeze
SELECTED = {'2-1-4' => ['euston', 1], '2-1-3' => ['ringsg', 2], '3-1-1' => ['pred', 3]}.freeze
PROFILES = ROOT.join('content/authors').glob('*/_index.md').to_h do |path|
  [path.parent.basename.to_s, read_page(path).first.fetch('title')]
end

def venue_for(source)
  return 'arXiv preprint' if source['tag'] == 'Preprint' || source['publication'] == 'Arxiv Preprint'
  short = source.fetch('tag').sub(/\s*\d{2}[a-z]?\z/, '')
  if short == 'ToN'
    return source.fetch('publication').start_with?('IEEE/ACM') ? 'IEEE/ACM ToN' : 'IEEE ToN'
  end
  VENUES.fetch(short) { raise "Unrecognized venue: #{source['tag']}" }
end

def topics_for(path, source)
  relative = path.relative_path_from(LEGACY)
  dirs = relative.each_filename.to_a[0...-1]
  topics = dirs.each_index.map do |index|
    folder = LEGACY.join(*dirs[0..index])
    page = folder.join('_index.md')
    page.exist? ? read_page(page).first.fetch('title') : dirs[index].split('_').map(&:capitalize).join(' ')
  end
  (topics + [source.fetch('Subtype')]).uniq
end

def write_record(path, metadata, abstract, body)
  # JSON flow values are valid YAML and keep the four required fields easy to edit.
  frontmatter = metadata.map { |key, value| "#{key}: #{JSON.generate(value)}" }.join("\n")
  prose = [abstract, body].compact.reject(&:empty?).join("\n\n")
  path.write("---\n#{frontmatter}\n---\n" + (prose.empty? ? '' : "\n#{prose}\n"))
end

source_files = LEGACY.glob('**/*.md').reject { |path| path.basename.to_s == '_index.md' }.sort
seen_titles = {}; seen_slugs = {}; records = []
source_files.each do |path|
  source, body = read_page(path)
  title = source.fetch('title')
  key = title.strip.downcase.gsub(/\s+/, ' ')
  raise "Duplicate title: #{path} and #{seen_titles[key]}" if seen_titles[key]
  seen_titles[key] = path
  selected = SELECTED[path.basename('.md').to_s]
  # Named systems retain recognizable short filenames. Other papers use the title.
  short_name = title.match(/\A([A-Za-z][A-Za-z0-9-]+): /)&.captures&.first
  slug = selected ? selected.first : slugify(short_name || title)
  raise "Duplicate filename: #{slug}" if seen_slugs[slug]
  seen_slugs[slug] = path
  authors = source.fetch('authors').map { |author| PROFILES.fetch(author, author) }
  result = {'title' => title, 'authors' => authors, 'venue' => venue_for(source), 'year' => Integer(source.fetch('date')[0, 4])}
  result['paper'] = source['doi'] if source['doi'] && !source['doi'].empty?
  (source['links'] || []).each do |link|
    case link.fetch('type')
    when 'code', 'pdf'
      raise "Repeated #{link['type']} link: #{path}" if result[link['type']]
      result[link['type']] = link.fetch('url')
    when 'preprint'
      raise "Unknown preprint provider: #{path}" unless link['provider'] == 'arxiv'
      raise "Preprint would overwrite paper link: #{path}" if result['paper']
      result['paper'] = "https://arxiv.org/abs/#{link.fetch('id')}"
    else
      raise "Unrecognized link type: #{link['type']} in #{path}"
    end
  end
  result['conference'] = source['conference_url'] if source['conference_url'] && !source['conference_url'].empty?
  result['award'] = source['award'] if source['award'] && !source['award'].empty?
  (source['author_notes'] || []).each_with_index do |note, index|
    next unless note && !note.empty?
    field = {'Corresponding Author' => 'corresponding', 'Equal contribution' => 'equal_contribution'}.fetch(note)
    (result[field] ||= []) << authors.fetch(index)
  end
  group_positions = source.fetch('authors').each_index.select do |index|
    id = source['authors'][index]
    PROFILES.key?(id) && id != 'liuzhuotao'
  end.map { |index| index + 1 }
  result['group_authors'] = group_positions unless group_positions.empty?
  result['topics'] = topics_for(path, source)
  if selected
    result['selected'] = true
    result['selected_order'] = selected.last
  end
  # Hugo's default path canonicalization lowercases the legacy mixed-case folder.
  result['aliases'] = ['/' + path.relative_path_from(ROOT.join('content')).sub_ext('').to_s.downcase + '/']
  write_record(OUTPUT.join("#{slug}.md"), result, source['abstract'], body)
  records << {source: path.relative_path_from(ROOT).to_s, file: "#{slug}.md", metadata: result,
              has_abstract: !!(source['abstract'] && !source['abstract'].empty?), source_keys: source.keys}
end

OUTPUT.join('migration-audit.json').write(JSON.pretty_generate(records) + "\n")
puts "Migrated #{records.length} unique publications (#{records.count { |r| r[:metadata]['selected'] }} selected) to #{OUTPUT}."
puts 'Source files are unchanged. Inspect the staged result before copying into the maintained collection.'
