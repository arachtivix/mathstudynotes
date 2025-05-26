(ns proj.p879.core
  (:gen-class))

(def board-width 4)
(def board-size (* board-width board-width))
; true -> number remains ; false -> number used up
(def starting-board (vec (repeat board-size true)))

(defn is-valid-pos
  [xy dim]
  (and (< (get xy 0) dim)
       (< (get xy 1) dim)
       (>= (get xy 0) 0)
       (>= (get xy 1) 0)))

(defn to-xy
  [pos]
  (vector (mod pos board-width) (int (/ pos board-width))))

(defn to-int
  [xy side-len]
  (let [x (get xy 0)
        y (get xy 1)]
    (+ (* side-len y) x)))

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

(defn scale-vec
  [xy sx sy]
  (let [x (get xy 0)
        y (get xy 1)]
    (vector (* sx x) (* sy y))))

(defn gen-all-vecs
  [pos-vecs]
  (cond
    (= (count pos-vecs) 0) '()
    :else (let [curr (first pos-vecs)
                tail (gen-all-vecs (rest pos-vecs))
                x (get curr 0)
                y (get curr 1)
                sv1 (scale-vec curr -1 1)
                sv2 (scale-vec curr 1 -1)
                sv3 (scale-vec curr -1 -1)]
            (conj tail curr sv1 sv2 sv3))))

(def all-vecs (into #{}
                    (gen-all-vecs unq-pos-vecs)))

(defn add-vecs
  [x1y1 x2y2]
  (let [x1 (get x1y1 0)
        y1 (get x1y1 1)
        x2 (get x2y2 0)
        y2 (get x2y2 1)]
    (vector (+ x1 x2) (+ y1 y2))))

(defn dir-vec
  [from-xy to-xy]
  (reduce-vec (add-vecs (scale-vec from-xy -1 -1) to-xy)))

(defn from-to
  [from-xy to-xy]
  (cond (= from-xy to-xy) (list to-xy)
        :else (let [dv (dir-vec from-xy to-xy)
                    next-place (add-vecs from-xy dv)]
                (cons from-xy (from-to next-place to-xy)))))

(def test-board-1
  [true true false
   true false false
   true false true])

(defn taken-by
  "get xy vecs for places taken going going 'from' exl 'to' incl"
  [from to board dim]
  (let [path (from-to from to)]
    (filter
     #(and (is-valid-pos % dim) (get board (to-int % dim)))
     (rest (from-to from to)))))

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn -main []
  (println "Solution to Problem 879:")
  (println (solve)))
