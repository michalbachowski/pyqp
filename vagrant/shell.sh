#!/bin/sh

# added missing symlink
`test ! -x /usr/bin/ruby && ln -s /opt/vagrant_ruby/bin/ruby /usr/bin/ruby`

# install packages via apt
if [ -x /usr/bin/apt-get ]; then
    # update
    apt-get update
    # ctags
    apt-get install exuberant-ctags 
    # python3
    apt-get install python3.2 python3.2-minimal
    # make
    apt-get install make
fi

# install packages via pip
if [ -x /usr/local/bin/pip ]; then
    # tox
    pip install tox
    # coverage
    pip install coverage
fi

# configure environment
su vagrant -c 'test ! -d ~/.termrc && git clone git://github.com/michalbachowski/termrc.git ~/.termrc && cd ~/.termrc && /bin/bash init.sh'
  
# configure vim
su vagrant -c 'test ! -d ~/.vimper && git clone git://github.com/michalbachowski/vimper.git ~/.vimper && cd ~/.vimper && python bootstrap.py'

# git config
su vagrant -c 'git config --global color.ui true'
su vagrant -c 'git config --global core.editor vim'

exit 0