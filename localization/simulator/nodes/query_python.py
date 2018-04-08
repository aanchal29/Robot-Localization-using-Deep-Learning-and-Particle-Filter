#!/usr/bin/env python

from sensing_model_and_map import *

def main():
    print "Testing gauss()..."
    print "\t", gauss(2.0, 3.0, 4.0)
    print "\t", gauss(5.5, 4.2, 6.3)

    print "Testing door()..."
    print "\t", door(4.4, 2.9)
    print "\t", door(1.745, 9.03)

    print "Testing p_door()..."
    print "\t", p_door(6.25)
    print "\t", p_door(0.23)

    print "Testing p_wall()"
    print "\t", p_wall(2.76)
    print "\t", p_wall(8.2)

if __name__ == '__main__':
    main()
