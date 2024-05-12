(ns p879.core
  (:gen-class))


(def board-width 4)
(def board-size (* board-width board-width))
; true -> number remains ; false -> number used up
(def starting-board (vec (repeat board-size true)))

(defn is-valid-pos
  [xy]
  (and (< (get xy 0) board-width)
       (< (get xy 1) board-width)
       (>= (get xy 0) 0)
       (>= (get xy 1) 0)))

(defn to-xy
  [pos]
  (vector (mod pos board-width) (int (/ pos board-width))))

(def all-coords
  (map to-xy (range board-size)))

(defn gcd
  [x y]
  (cond
    (= 0 x) y
    (= 0 y) x
    (> x y) (recur y x)
    :else (recur x (mod y x))))

(defn reduce-vec
  [xy]
  (let [x (get xy 0)
        y (get xy 1)
        d (gcd x y)]
    (cond
      (= 0 x) [0 1]
      (= 0 y) [1 0]
      :else (vector (/ x d) (/ y d)))))

(def unq-pos-vecs
   (into #{}
        (map
         reduce-vec
         all-coords)))

(defn gen-all-vecs
  [pos-vecs]
  (cond
    (= (count pos-vecs) 0) '()
    :else (let [curr (first pos-vecs)
                tail (gen-all-vecs (rest pos-vecs))
                x (get curr 0)
                y (get curr 1)
                neg-vec (cond (= x 0) (list x (* -1 y))
                              :else (list (* -1 x) y))]
            (conj tail curr (into [] neg-vec)))))

(def all-vecs (gen-all-vecs unq-pos-vecs))
