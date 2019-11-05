#!/bin/bash
# script adapts auto-generated meta.yaml from running
# ```Bash
#   conda skeleton pypi --noarch-python ibmpairs
# ```
# for pull request to conda-forge (https://github.com/conda-forgei/staged-recipes)
#
# Copyright 2019 Physical Analytics, IBM Research All Rights Reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

# script constants
IBMPAIRS_CONDA_PACKAGE_MAINTAINER_GITHUB_ID='cmalbrec'
IBMPAIRS_LICENSE_FILE_NAME='LICENSE'
IBMPAIRS_DOCUMENTATION_URL='https://pairs.res.ibm.com/tutorial/'
IBMPAIRS_OPENSOURCE_DEVELOPMENT_URL='https://github.com/ibm/ibmpairs'

# parse input parameters
# conda build meta file to adapt
condaMetaFile="${1-'meta.yaml'}"

# set conda package maintainer
sed \
    -i 's/your-github-id-here/'"$IBMPAIRS_CONDA_PACKAGE_MAINTAINER_GITHUB_ID/" \
    "$condaMetaFile"

# adapt license details
sed \
    -i 's/license_file:.*$/license_file: '"$IBMPAIRS_LICENSE_FILE_NAME/" \
    "$condaMetaFile"

# set documentation info
sed \
    -i 's~doc_url:.*$~doc_url: "'"$IBMPAIRS_DOCUMENTATION_URL"'"~' \
    "$condaMetaFile"
sed \
    -i 's~dev_url:.*$~dev_url: "'"$IBMPAIRS_OPENSOURCE_DEVELOPMENT_URL"'"~' \
    "$condaMetaFile"

exit 0
