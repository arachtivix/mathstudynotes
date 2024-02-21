#! /usr/bin/mixguile \
-e main -s
!#

(define (ct-nonzero-lines s e)
  (define subct (cond ((> s e) 0)
		       (else (ct-nonzero-lines (+ 1 s) e))))
  (cond ((or (> s e) (= (mix-cell s) 0)) subct)
	(else (+ 1 subct))))

(define (dw-mix-byte-divisor p)
  (expt 64 (- 5 p)))

(define (dw-mix-byte-from-args n pos)
  (define divisor (dw-mix-byte-divisor pos))
  (modulo (quotient n divisor) 64))

(define (dw-mix-word n)
  (define b1 (dw-mix-byte-from-args n 1))
  (define b2 (dw-mix-byte-from-args n 2))
  (define b3 (dw-mix-byte-from-args n 3))
  (define b4 (dw-mix-byte-from-args n 4))
  (define b5 (dw-mix-byte-from-args n 5))
  (list b1 b2 b3 b4 b5))

; credit: stack overflow https://stackoverflow.com/questions/22060239/scheme-function-to-reverse-a-list
(define (reverse lst)
  (reverse-helper lst '()))

(define (reverse-helper lst acc)
  (if (null? lst)
      acc
      (reverse-helper (cdr lst) (cons (car lst) acc))))

(define (run-test program input-value)
  (mix-compile program)
  (define instruction-count (ct-nonzero-lines 0 3999))
  (define ret (list instruction-count))
  (display "test value ")
  (display input-value)
  (display " received\n")
  (display "test value mix bytes: ")
  (display (reverse (dw-mix-word input-value)))
  (newline)
  (mix-load program)
  (mix-smem 200 input-value)
  (mix-run)
  (mix-preg)
  (mix-pmem "200-210")
  ret)


(define (main arg1)
  (display (run-test "solution" 123456789))
  (newline)
  (display (run-test "solution_2" 123456789))
  (newline)
  (display (run-test "book_solution1" 123456789)))
