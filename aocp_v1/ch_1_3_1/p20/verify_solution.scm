#! /usr/bin/mixguile \
-e main -s
!#

(define (ver loc val) (= (mix-cell loc) val))

(define disp-check
  (lambda (loc)
    (define is-good (ver loc 133))
    (if is-good
        (display (string-append (number->string loc) " :) Success\n"))
        (display (string-append (number->string loc) " :( Failure\n")))
    is-good))

(define (disp-check-range start end)
  (cond
    ((and (>= end start) (disp-check start)) (disp-check-range (+ start 1) end))
    ((> start end) #t)
    (else #f)
  )
)

(define main
  (lambda (args)
    (mix-load "aocp_v1_ch1.3.1_p20")
    (mix-sreg "I4" 123)
    (mix-run)
    (mix-pall)
    (disp-check-range 0 3999)))