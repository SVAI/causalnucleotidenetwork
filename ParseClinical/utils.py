from __future__ import print_function, absolute_import, unicode_literals
from collections import deque
import glob
import os


def find_all_matches(target_dir, filename, glob_pattern=False, abs_path=False, exclude_dirs=[]):
    """
    Arguments:
        target_dir (:obj:`str`): Directory to start search in.
        filename (:obj:`str`): file name to match
        glob_pattern (:obj:`bool`): The filename is a unix glob pattern
        exclude_dirs (:obj:`list`): directories to exclude from matches

    Returns:
        list of absolute paths to files matching filename

    Examples:
        >>> find_all_matches(target_dir='Test_Data', filename='files.2018-05-19.json')
        [u'Test_Data/files.2018-05-19.json']
        >>> find_all_matches(target_dir='Test_Data', filename='*2018*.json', glob_pattern=True)
        [u'Test_Data/files.2018-05-19.json']
    """
    def _normal_match():
        if filename in files:
            path = os.path.join(root, filename)
            matches.append(os.path.abspath(path) if abs_path else path)

    def _glob_pattern_match():
        glob_matches = glob.glob(os.path.join(root, filename))
        glob_matches = [os.path.abspath(path) for path in glob_matches] if abs_path else glob_matches

        if glob_matches:
            matches.extend(glob_matches)

    _match_handler = _glob_pattern_match if glob_pattern else _normal_match
    matches = []
    for root, dirs, files in os.walk(target_dir):
        _match_handler()

        for dir_ex in exclude_dirs:
            if dir_ex in dirs:
                dirs.remove(dir_ex)
    return matches


def search_for_key(target_key, mapping, contains=True):
    """Search dictionary for a specific key, optionally pattern match (TBD)

    Returns:
        Full path to key in array
        ['key1', 'key2', 'key3']

    TODO:
        - So sloppy with the memory usage
        - Not done
    """
    def containing_match():
        pass

    def exact_match():
        pass

    key_paths = []
    curr_path = []
    match_func = containing_match if contains else exact_match

    iterators = deque()
    iterators.append(mapping.iteritems())
    while True:
        try:
            curr_key, curr_value = next(iterators[-1])
            curr_path.append(curr_key)
            if match_func(target_key, curr_key):
                return curr_path[-1]
            iterators.append(curr_value.itervalues())
        except AttributeError:  # not a dict, end of path, key not found
            curr_path = []
        except StopIteration:
            iterators.pop()
            if not iterators:
                break


if __name__ == '__main__':
    import doctest
    doctest.testmod()
