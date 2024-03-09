#! /usr/bin/mixguile \
-e main -s
!#

(define face-up 0)
(define face-down 1)

(define clubs 1)
(define diamonds 2)
(define hearts 3)
(define spades 4)

(define ace 1)
(define jack 11)
(define queen 12)
(define king 13)

(define (card-numerical tag suit rank next)
  (+ (ash tag 24)
     (ash suit 18)
     (ash rank 12)
     next))

(define (place-card tag suit rank next loc)
  (define cell-val (card-numerical tag suit rank next))
  (mix-smem loc cell-val))

(define (run-test top-var expected)
    (display "Starting test")
    (mix-compile program)
    (mix-load program)
    (place-card face-up diamonds 2 386 242)
    (mix-smem 1000 top-var) ; telling MIX what the TOP variable is
    (display "TOP = ")
    (display (mix-cell 1000)) ; location of TOP -- currently 242
    (display "\nNEWCARD = ")
    (display (mix-cell 1001)) ; location of NEWCARD -- not set yet
    (newline)
    (place-card face-up spades 3 100 386)
    (place-card face-down clubs 10 0 100)
    (mix-run)
    (display "RESULTS:\n")
    (display "TOP = ")
    (display (mix-cell 1000)) ; TOP again -- should be 386
    (display "\nNEWCARD = ")
    (display (mix-cell 1001)) ; NEWCARD -- should be 242
    (newline)
    (mix-pmem 0 1)
    (mix-pmem 1000 1001)
    (mix-pmem 386)
    (mix-preg)
    (display "Expected ")
    (display expected)
    (display " in pmem 1000\n\n"))

(define program "solution")
(define main
  (lambda (args)
    (run-test 242 386) ; TOP is from scenario 3 in the book
    (run-test 0 0)))
