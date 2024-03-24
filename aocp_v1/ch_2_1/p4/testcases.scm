#! /usr/bin/mixguile \
-e main -s
!#

(load "scenarios.scm")

(define (run-test scenario program)
  (mix-compile program)
  (mix-load program)
  (define expected (scenario))
  (display "Starting conditions:\n")
  (mix-preg)
  (mix-pmem 1000 1005)
  (display "Starting test")
  (mix-run)
  (expected))

(define main
  (lambda (args)
    (run-test scen1 "solution")
    (run-test scen2 "solution")
    (run-test scen3 "solution")))
