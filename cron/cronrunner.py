#! /usr/bin/env python
"""Simple cronjob scaffolding.

This is basically a small wrapper around subprocess to run a command,
capture reporting any return status, error, or output, and put them
somewhere useful/accessible.

  usage:
    cron-runner.py [opts] cmd [cmd_opts..]
  options:
    -l dir: create a <name>.latest.txt symlink in this dir
    -n name: the name for the report (default: command argv[0])
    -o dir: output directory for path (default: cwd)
"""

import datetime
import django
import django.conf
import django.template
import django.template.loader
import getopt
import os
import subprocess
import sys


def Usage(error_message=None):
  if error_message:
    fh = sys.stderr
    fh.write(error_message + '\n\n')
  else:
    fh = sys.stdout
  fh.write(__doc__ + '\n')
  fh.flush()

def RunCommand(args, name, output_dir):
  now = datetime.datetime.now()
  timestamp = datetime.datetime.strftime(now, '%Y%m%d-%H%M%S')
  output_filename = '%s-%s.txt' % (name, timestamp)
  output_path = os.path.sep.join([output_dir, output_filename])
  stdout_path = os.path.sep.join([
      output_dir,
      '%s-%s.STDOUT' % (name, timestamp)])
  stderr_path = os.path.sep.join([
      output_dir,
      '%s-%s.STDERR' % (name, timestamp)])

  with file(stdout_path, 'w') as stdout_fh, file(stderr_path, 'w') as stderr_fh:
    proc = subprocess.Popen(args, stderr=stderr_fh, stdout=stdout_fh)
    retvalue = proc.wait()
  template = django.template.loader.get_template('output.tmpl')
  context = django.template.Context(dict(
      command=" ".join(args), name=name, now=now, retvalue=retvalue,
      stderr=file(stderr_path, 'r').read(),
      stdout=file(stdout_path, 'r').read()))
  rendered = template.render(context)
  file(output_path, 'w').write(rendered)
  return output_path


if __name__ == '__main__':
  project_root = os.path.dirname(os.path.realpath(sys.argv[0]))
  django.conf.settings.configure(
      TEMPLATE_DIRS=[os.path.sep.join([project_root, 'templates'])])
  django.setup()

  try:
    opts, args = getopt.getopt(sys.argv[1:], 'hl:n:o:')
  except getopt.GetoptError as e:
    Usage(error_message=str(e))
    sys.exit(1)

  name, output_dir, symlink_dir = None, None, None
  for opt, val in opts:
    if opt == '-h':
      Usage()
      sys.exit(0)
    elif opt == '-l':
      symlink_dir = val
    elif opt == '-n':
      name = val
    elif opt == '-o':
      output_dir = val

  if not args:
    raise Exception('lol you need to tell me to run something')
  name = name or args[0]
  output_dir = output_dir or os.curdir

  report_filename = RunCommand(args, name=name, output_dir=output_dir)
  if symlink_dir:
    symlink_name = '%s.latest.txt' % name
    symlink_path = os.path.sep.join([symlink_dir, symlink_name])
    if os.path.exists(symlink_path):
      os.unlink(symlink_path)
    os.symlink(report_filename, symlink_path)
