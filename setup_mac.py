import py2app
# Build the .app file
setup(
  options=dict(
    py2app=dict(
      iconfile='NoTagApp.icns',
      packages='wx',
      site_packages=True,
      plist=dict(
        CFBundleName = "NoTagApp",
        CFBundleShortVersionString = "0.0.1",     # must be in X.X.X format
        CFBundleGetInfoString = "NoTagApp 0.0.1",
        CFBundleExecutable = "NoTagApp",
        CFBundleIdentifier = "eu.loicwolff.notagapp",
        CFBundleIconFile = 'NoTagApp.icns'
        #CFBundleDocumentTypes = [dict(CFBundleTypeExtensions=["*"])]
      ),
    ),
  ),
  app=[ 'NoTagApp.py' ]
)

