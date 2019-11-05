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
IBMPAIRS_LICENSE='BSD-3-Clause'
IBMPAIRS_DOCUMENTATION_URL='https://pairs.res.ibm.com/tutorial/'
IBMPAIRS_OPENSOURCE_DEVELOPMENT_URL='https://github.com/ibm/ibmpairs'
EXIT_FAILURE=1
EXIT_SUCCESS=0

# parse input parameters
# conda build meta file to adapt
condaMetaFile="${1-'meta.yaml'}"

# set conda package maintainer
sed \
    -i 's/your-github-id-here/'"$IBMPAIRS_CONDA_PACKAGE_MAINTAINER_GITHUB_ID/" \
    "$condaMetaFile" || \
{ echo "ERROR: Failed setting conda-forge package maintainer: '$IBMPAIRS_CONDA_PACKAGE_MAINTAINER_GITHUB_ID'"; exit $EXIT_FAILURE; }

# adapt license details
sed \
    -i 's/license_file:.*$/license_file: '"$IBMPAIRS_LICENSE_FILE_NAME/" \
    "$condaMetaFile" || \
{ echo "ERROR: Failed setting ibmpairs package license file name: '$IBMPAIRS_LICENSE_FILE_NAME'"; exit $EXIT_FAILURE; }
sed \
    -i 's/license:.*$/license: "'"$IBMPAIRS_LICENSE"'"/' \
    "$condaMetaFile" || \
{ echo "ERROR: Failed setting ibmpairs package license: '$IBMPAIRS_LICENSE'"; exit $EXIT_FAILURE; }

# set documentation info
sed \
    -i 's~doc_url:.*$~doc_url: "'"$IBMPAIRS_DOCUMENTATION_URL"'"~' \
    "$condaMetaFile" || \
{ echo "ERROR: Failed setting ibmpairs documentation URL: '$IBMPAIRS_DOCUMENTATION_URL'"; exit $EXIT_FAILURE; }
sed \
    -i 's~dev_url:.*$~dev_url: "'"$IBMPAIRS_OPENSOURCE_DEVELOPMENT_URL"'"~' \
    "$condaMetaFile" || \
{ echo "ERROR: Failed setting ibmpairs developer URL: '$IBMPAIRS_OPENSOURCE_DEVELOPMENT_URL'"; exit $EXIT_FAILURE; }

# remove required modules for testing, because we simply perform an import
awk -i inplace \
    '$1 == "test:"{t=1}
    t==1 && $1 == "requires:"{t++; next}
    t==2 && /:[[:blank:]]*$/{t=0}
    t != 2' \
    "$condaMetaFile" || \
{ echo "ERROR: Failed cleaning testing requirements."; exit $EXIT_FAILURE; }

exit $EXIT_SUCCESS
