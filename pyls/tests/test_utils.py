import pytest
from pyls.utils import human_readable_size, filter_directory_contents, sort_directory_contents, get_target_item


def test_human_readable_size():
    assert human_readable_size(0) == '0.0 B'
    assert human_readable_size(2 ** 10) == '1.0 KB'
    assert human_readable_size(2 ** 10 - 1) == '1023.0 B'
    assert human_readable_size(2 ** 10 + 100) == '1.1 KB'
    assert human_readable_size(2 ** 20) == '1.0 MB'
    assert human_readable_size(2 ** 30) == '1.0 GB'
    assert human_readable_size(2 ** 40) == '1.0 TB'
    assert human_readable_size(2 ** 50) == '1.0 PB'


def test_human_readable_size_invalid_inputs():
    with pytest.raises(TypeError, match="Size must be an integer."):
        human_readable_size("1024")

    with pytest.raises(TypeError, match="Size must be an integer."):
        human_readable_size(1024.1)

    with pytest.raises(ValueError, match="Size must not be negative."):
        human_readable_size(-1024)


def test_filter_directory_contents():
    directory = {
        'contents': [
            {'name': 'file1', 'contents': []},
            {'name': 'file2'},
            {'name': '.hidden_file'},
        ]
    }
    filtered = filter_directory_contents(directory)
    assert len(filtered) == 2
    assert all(not item['name'].startswith('.') for item in filtered)

    filtered_with_hidden = filter_directory_contents(directory, include_hidden=True)
    assert len(filtered_with_hidden) == 3

    filtered_files = filter_directory_contents(directory, filter_type='file')
    assert len(filtered_files) == 1
    assert filtered_files[0]['name'] == 'file2'

    filtered_dirs = filter_directory_contents(directory, filter_type='dir')
    assert len(filtered_dirs) == 1
    assert filtered_dirs[0]['name'] == 'file1'

    directory_without_contents = {}
    filtered_empty = filter_directory_contents(directory_without_contents)
    assert filtered_empty == []

    directory_with_none_contents = {'contents': None}
    with pytest.raises(TypeError):
        filter_directory_contents(directory_with_none_contents)



def test_sort_directory_contents():
    directory_items = [
        {'name': 'fileB', 'time_modified': 100},
        {'name': 'fileA', 'time_modified': 200},
        {'name': 'fileC', 'time_modified': 50},
    ]

    sorted_by_name = sort_directory_contents(directory_items)
    assert [item['name'] for item in sorted_by_name] == ['fileA', 'fileB', 'fileC']

    sorted_by_time = sort_directory_contents(directory_items, sort_by='time_modified')
    assert [item['time_modified'] for item in sorted_by_time] == [50, 100, 200]

    reverse_sorted_by_name = sort_directory_contents(directory_items, reverse=True)
    assert [item['name'] for item in reverse_sorted_by_name] == ['fileC', 'fileB', 'fileA']

    reverse_sorted_by_time = sort_directory_contents(directory_items, sort_by='time_modified', reverse=True)
    assert [item['time_modified'] for item in reverse_sorted_by_time] == [200, 100, 50]

    incomplete_items = [
        {'name': 'fileA'},
        {'time_modified': 100},
    ]
    with pytest.raises(KeyError, match="'name'"):
        sort_directory_contents(incomplete_items)

    assert sort_directory_contents([]) == []


def test_sort_directory_contents_invalid_key():
    directory_items = [
        {'name': 'fileB', 'time_modified': 100},
        {'name': 'fileA', 'time_modified': 200},
        {'name': 'fileA', 'time_modified': '300'},
    ]

    with pytest.raises(KeyError):
        sort_directory_contents(directory_items, sort_by='invalid_key')


def test_get_target_item():
    root_directory = {
        'name': '',
        'contents': [
            {
                'name': 'dir1',
                'contents': [
                    {'name': 'file1'},
                    {'name': 'file2'},
                ]
            },
            {
                'name': 'dir2',
                'contents': [
                    {'name': 'file3'},
                ]
            },
            {'name': 'file4'}
        ]
    }

    assert get_target_item(root_directory, '') == root_directory

    target = get_target_item(root_directory, 'dir1/file1')
    assert target == {'name': 'file1'}

    target = get_target_item(root_directory, 'dir2')
    assert target == {
        'name': 'dir2',
        'contents': [{'name': 'file3'}]
    }

    target = get_target_item(root_directory, 'dir1/nonexistent_file')
    assert target is None

    target = get_target_item(root_directory, 'nonexistent_dir')
    assert target is None

    target = get_target_item(root_directory, 'dir1/nonexistent_dir/file')
    assert target is None

    target = get_target_item(root_directory, 'file4/file_inside')
    assert target is None

    target = get_target_item(root_directory, 'dir1/dir2/file5')
    assert target is None