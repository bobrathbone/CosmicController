#!/bin/bash
# $Id: build.sh,v 1.2 2018/05/26 11:46:48 bob Exp $
# Build script for the Raspberry PI radio
# Run this script as user pi and not root

# Install the following packages before using this script
# sudo apt-get -y install equivs apt-file lintian

# Compatability rules
# Edit the compat file and chjange 7 to 9
# sudo vi /usr/share/equivs/template/debian/compat (Replace 7 with 9)

PKGDEF=cosmicd
PKG=cosmicd
VERSION=$(grep ^Version: ${PKGDEF} | awk '{print $2}')
ARCH=$(grep ^Architecture: ${PKGDEF} | awk '{print $2}')
DEBPKG=${PKG}_${VERSION}_${ARCH}.deb
BUILDLOG=build.log

# Tar build files
BUILDFILES="cosmicd cosmicd.postinst cosmicd.postrm cosmicd.preinst"

echo "Building package ${PKG} version ${VERSION}" | tee ${BUILDLOG}
echo "from input file ${PKGDEF}" | tee -a ${BUILDLOG}
sudo chown pi:pi *.py *.sh
sudo chmod +x  *.py *.sh

# Build the package
equivs-build ${PKGDEF} | tee -a ${BUILDLOG}

echo -n "Check using Lintian y/n: "
read ans
if [[ ${ans} == 'y' ]]; then
	echo "Checking package ${DEBPKG} with lintian"  | tee -a ${BUILDLOG} 
	lintian ${DEBPKG} | tee -a ${BUILDLOG}
	if [[ $? = 0 ]]
	then
	    echo "Package ${DEBPKG} OK" | tee -a ${BUILDLOG}
	    echo "See ${BUILDLOG} for build details" 
	    echo "Package ${DEBPKG} file list" >> ${BUILDLOG}
	    dpkg -c ${DEBPKG} >> ${BUILDLOG}
	else
	    echo "Package ${DEBPKG} has errors" | tee -a ${BUILDLOG}
	fi
fi

# End of build script
