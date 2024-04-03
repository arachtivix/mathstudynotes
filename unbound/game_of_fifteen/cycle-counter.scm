#! /usr/bin/mixguile \
-e main -s
!#

(define (traverse-cycle start-idx curr-idx input output)
  (define nxt (vector-ref input curr-idx))
  (cond ((= -1 (vector-ref output curr-idx))
	 (vector-set! output curr-idx start-idx)
	 (traverse-cycle start-idx nxt input output))))

(define (eval-upto idx upto input output)
  (traverse-cycle idx idx input output)
  (if (<= (+ 1 idx) upto)
      (eval-upto (+ 1 idx) upto input output)))

(define (count-cycles vec)
  (display vec)
  (define vlen (vector-length vec))
  (define cycle-start (make-vector vlen -1))
  (newline)
  (display vlen)
  (newline)
  (display cycle-start)
  (newline)
  (eval-upto 0 (- vlen 1) vec cycle-start)
  (display cycle-start)
  (newline))

(define main
  (lambda (args)
    (display "counting cycles")
    (newline)
    (define input #(2 0 1 3 4))
    (count-cycles input)
    (newline)))
