# AlexandrosV
alias vi='vim -p'
alias ll='date;ls -ltr  --color=tty'
alias grep='grep --color=always'
alias egrep='egrep --color=always'

export HISTCONTROL=erasedups:ignoreboth
export HISTCONTROL=ignoreboth
export HISTFILE=~/.bash_history HISTSIZE=1000000 HISTFILESIZE=1000000 HISTIGNORE=?:??
export FIGNORE="history:download:old:orig:org:bk:bkup:OLD:pid"
export GLOBIGNORE=${FIGNORE}

alias u='cd ..'
alias cd..='cd ..'
alias ..='cd ..'
alias ll='ls -Gltr'

shopt -s histappend
shopt -s cdspell

# http://bashrcgenerator.com/
# Short basic one 
#export PS1="\W \$"
# Long version
export PS1="\[\033[38;5;1m\]\u\[$(tput sgr0)\]\[\033[38;5;15m\]:\[$(tput sgr0)\]\[\033[38;5;2m\]\W\[$(tput sgr0)\]\[\033[38;5;15m\]\\$\[$(tput sgr0)\]"

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi
