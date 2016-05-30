import atexit, os, pip, shutil, sys, tempfile, zipfile

def die(s):
    print(s)
    sys.exit(1)
if __name__ != '__main__':
    die('This script must be run standalone')
if len(sys.argv) != 3:
    die('Usage: %s <path to requirements.txt> <output path.zip>' % sys.argv[0])
if not sys.argv[2].endswith('.zip'):
    die('Invalid output .zip path')
if int(pip.__version__[0]) < 8:
    print('You are using pip < 8, which has not been tested. Package installation in a temporary folder may fail.')

tmpdir = tempfile.mkdtemp()
@atexit.register
def cleanup():
    print('cleaning ' + tmpdir)
    shutil.rmtree(tmpdir)

def pip_run(*args):
    try:
        print('==> pip ' + ' '.join(args))
        pip.main(list(args))
    except SystemExit:
        die('*** pip failed')

pip_run('install', '-r', sys.argv[1], '--target', tmpdir)
shutil.make_archive(os.path.splitext(sys.argv[2])[0], 'zip', root_dir=tmpdir, verbose=1)
