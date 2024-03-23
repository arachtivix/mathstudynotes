

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

(define newcard 1000) ; location of the NEWCARD variable in the MIX machine
(define top 1001) ; location of the TOP variable in the MIX machine
(define LAMBDA 0) ; the aocp uppercase lambda/list end marker

(define (card-numerical tag suit rank next)
  (+ (ash tag 24)
     (ash suit 18)
     (ash rank 12)
     next))

(define (place-card tag suit rank next loc)
  (define cell-val (card-numerical tag suit rank next))
  (mix-smem loc cell-val))



(define (scen1)
  (place-card face-up spades 2 101 100) ; top card
  (place-card face-down spades 3 102 101)
  (place-card face-down spades 4 103 102)
  (place-card face-down hearts queen 104 103)
  (place-card face-down diamonds jack LAMBDA 104)
  ; NEWCARD value set at next position but not linked up yet
  (place-card face-up clubs king LAMBDA 105)
  (mix-smem newcard 105)
  (mix-smem top 100)
  (lambda ()
    (mix-preg)
    (mix-pmem 100 108)
    (mix-pmem 1000 1005)
    (display "Expected ")
    (newline)
    (display (card-numerical face-down diamonds jack 105))
    (newline)
    (display (card-numerical face-down clubs king LAMBDA))
    (newline)
    (display "in memory locations 104 and 105 respectively\n")))
