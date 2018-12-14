from urllib.parse import quote, urlsplit, urlunsplit


def remove_beginning(url):
    if url.startswith('https://'):
        return 'https://', url[8:]
    elif url.startswith('http://'):
        return 'http://', url[7:]
    return '', url


def get_updir(url, level):
    prefix, url = remove_beginning(url)
    splitted = url.split('/')
    if len(splitted) <= level + 1:
        return splitted[0] + '/'
    return prefix + '/'.join(splitted[:-(level+1)]) + '/'


def is_relative_link(url):
    return not url.startswith('https://') and not url.startswith('http://')


def make_absolute_path(url, relative_path):
    if relative_path.startswith('//'):
        prefix, url = remove_beginning(url)
        return prefix + relative_path[2:]
    if relative_path.startswith('/'):
        prefix, url = remove_beginning(url)
        return prefix + url.split('/')[0] + relative_path
    splitted_relative_path = relative_path.split('/')
    dir_to_up = splitted_relative_path.count('..')
    parent_directory = get_updir(url, dir_to_up)
    return parent_directory + '/'.join(splitted_relative_path[dir_to_up:])


def iri_to_uri(iri):
    parts = urlsplit(iri)
    uri = urlunsplit((
        parts.scheme,
        parts.netloc.encode('idna').decode('ascii'),
        quote(parts.path),
        quote(parts.query, '='),
        quote(parts.fragment),
    ))
    return uri