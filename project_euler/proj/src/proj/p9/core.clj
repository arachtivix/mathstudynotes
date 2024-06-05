(ns p9.core)

(def max-c 997)
(def max-c-sq (* max-c max-c))

(def squares-seq
  (take-while #(<= % max-c-sq) (map #(* % %) (iterate inc 1))))

(def sq-to-c
  (reduce
   (fn [prv n]
     (assoc prv (* n n) n))
   {}
   (range 1 (+ max-c 1))))

(defn is-sq
  [n]
  (get sq-to-c n))

(defn sqs-up-to
  [n]
  (take-while #(<= % n) squares-seq))

(defn abcs
  [n]
  (reduce
   (fn [coll sq]
     (if (and (is-sq (- n sq)) (<= (- n sq) sq))
       (let [a (get sq-to-c (- n sq))
             b (get sq-to-c sq)
             c (get sq-to-c n)]
         (cons [a b c] coll))
       coll))
   '()
   (sqs-up-to (- n 1))))

(defn all-abcs
  [n]
  (reduce
   (fn [coll sq]
     (concat (abcs sq) coll))
   '()
   (sqs-up-to n)))

(def answ-abc
  (take 1
        (filter
         #(= 1000 (apply + %))
         (all-abcs max-c-sq))))

(let [ans-vec (first answ-abc)
      a (get ans-vec 0)
      b (get ans-vec 1)
      c (get ans-vec 2)]
  (println "answ " [a b c] " -> " (* a b c)))
