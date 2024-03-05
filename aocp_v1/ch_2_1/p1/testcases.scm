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

(define program "solution")
(define main
  (lambda (args)
    (mix-compile program)
    (mix-load program)
    (place-card face-up spades ace 0 100)
    (mix-pmem 100)
    (mix-run)))
