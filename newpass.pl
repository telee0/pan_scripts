#!/usr/bin/perl -w

#
# newpass.pl [20220623]
#
#

use strict;
use Getopt::Std;

my $n = 8;
# my $n = 32;

my @chars = ('a' .. 'f', 0 .. 9);
my ($passwd, $salt);

my $usage = "Usage: $0 [-h] [-l len] [-c charset] [-v] [passwd]";

my %args;
my $verbose = 0;

#
#
#

getopts('c:hl:v', \%args);

if (defined($args{h})) {
	print $usage, "\n";
	print "\n";
	print "Character sets:\n";
	print '1. ("a" .. "f", 0 .. 9)', "\n";
	print '2. ("A" .. "Z", "a" .. "z", 0 .. 9)', "\n";
	print '3. ("A" .. "Z", 0 .. 9)', "\n";
	print '4. ("A" .. "Z", "a" .. "z", 0 .. 9, qw(! @ $ % ^ & * [ ]))', "\n";
	print "\n";
	exit;
}

if (defined($args{c}) && $args{c} > 0) {
	if ($args{c} == 2) {
		@chars = ('A' .. 'Z', 'a' .. 'z', 0 .. 9);
	} elsif ($args{c} == 3){
		@chars = ('A' .. 'Z', 0 .. 9);
	} elsif ($args{c} == 4){
		@chars = ('A' .. "Z", 'a' .. 'z', 0 .. 9, qw(! @ $ % ^ & * [ ]));
	}
}

if (defined($args{l}) && $args{l} > 0) {
    $n = $args{l};
}

if (defined($args{v})) {
	$verbose = 1;
}

#
#
#

if (@ARGV < 1) {
	srand;
	$passwd = join '', @chars[map {rand @chars} (1 .. $n)];
} else {
	$passwd = $ARGV[0];
}

if ($verbose) {
	@chars = ('a' .. 'z', 'A' .. 'Z', 0 .. 9, qw(. /));
	srand;
	$salt = join '', @chars[map {rand @chars} (1 .. 2)];

	print "passwd = $passwd\n";
	print "crypt  = ", crypt($passwd, $salt), "\n";
} else {
	print "$passwd\n";
}

