import os
import pytest
from rosdistro import get_index, get_distribution_file
from rosdistro.release_repository_specification import ReleaseRepositorySpecification
from rosdistro.distribution_file import DistributionFile


def test_release_repository_standard_naming():
    data = {
        'url': 'https://github.com/ros2-gbp/common_interfaces-release.git',
        'version': '5.9.2-2',
        'tags': {'release': 'release/rolling/{package}/{version}'},
        'packages': ['std_msgs']
    }
    repo = ReleaseRepositorySpecification('common_interfaces', data)
    repo.origin_distro = 'lyrical'
    
    assert repo.get_binary_package_name('std_msgs') == 'ros-lyrical-std-msgs'
    assert repo.target_distro_name == 'lyrical'


def test_release_repository_explicit_override():
    data = {
        'url': 'https://github.com/gazebosim/gz-cmake-release.git',
        'version': '5.1.1-2',
        'tags': {'release': 'gz-cmake5_{version}'},
        'packages': ['gz-cmake'],
        'binary_name': 'libgz-cmake5-dev'
    }
    repo = ReleaseRepositorySpecification('gz-cmake', data)
    repo.origin_distro = 'jetty'
    
    assert repo.get_binary_package_name('gz-cmake') == 'libgz-cmake5-dev'


def test_release_repository_custom_template():
    data = {
        'url': 'https://github.com/custom/repo-release.git',
        'version': '1.0.0-1',
        'tags': {'release': '{package}/{version}'},
        'packages': ['my_pkg'],
        'binary_prefix_template': 'custom-{distro}-{package}'
    }
    repo = ReleaseRepositorySpecification('custom_repo', data)
    repo.origin_distro = 'jazzy'
    
    assert repo.get_binary_package_name('my_pkg') == 'custom-jazzy-my-pkg'


def test_release_repository_non_ros_no_op():
    data = {
        'url': 'https://github.com/gazebosim/gz-sim-release.git',
        'version': '10.5.0-1',
        'tags': {'release': '{package}/{version}'},
        'packages': ['gz-sim10']
    }
    repo = ReleaseRepositorySpecification('gz-sim', data)
    repo.origin_distro = 'jetty'
    repo.distribution_type = 'gazebo'
    
    assert repo.get_binary_package_name('gz-sim10') == 'gz-sim10'


def test_distribution_file_binary_naming():
    dist_data = {
        'type': 'distribution',
        'version': 3,
        'release_platforms': {'ubuntu': ['noble']},
        'repositories': {
            'ros_tutorials': {
                'release': {
                    'url': 'https://github.com/ros-gbp/ros_tutorials-release.git',
                    'version': '1.0.0-1',
                    'tags': {'release': '{package}/{version}'},
                    'packages': ['turtlesim']
                }
            }
        }
    }
    dist_file = DistributionFile('lyrical', dist_data)
    assert dist_file.get_binary_package_name('turtlesim') == 'ros-lyrical-turtlesim'
