(ns proj.shared)

;; Functions for finding repeating decimal expansions
;; Takes a numerator and denominator and returns a lazy sequence of [numerator denominator] pairs
;; representing the long division process
(defn dec-exp-components [[n m]]
  (lazy-seq (let [r (rem n m)] (cons [n m] (dec-exp-components [(* 10 r) m])))))

;; Finds a repeating pattern in a sequence by tracking seen values in a map.
;;  Returns [end start] where end is the position where the repeat was found and start is where it began
(defn find-repeat [s m pos]
  (let [curr (first s)]
    (if (some? (m curr))
      [pos (m curr)]
      (recur (rest s) (assoc m curr pos) (+ 1 pos)))))

;; Returns the given sequence up to the first single element repeat (not including the repeated)
(defn get-seq-before-repeat
  ([s] (reverse (get-seq-before-repeat s #{} '())))
  ([s seen r] (let [f (first s)]
    (if (or (nil? f) (some? (seen f)))
      r
      (recur (rest s) (conj seen f) (cons f r))))))

(defn up-by-twos
  [start] (lazy-seq (cons start (up-by-twos (+ start 2)))))

(defn get-check-range
  [n]
  (conj
   (take-while #(<= (* % %) n) (up-by-twos 3))
   2))

(defn get-factors
  ([n] (get-factors n (get-check-range n)))
  ([n [first-factor & remain :as try-factors]]
   (cond (= 1 n)
         '()
         (= 0 (count try-factors))
         (list n)
         (= 0 (mod n first-factor))
         (let [nn (/ n first-factor)]
           (conj (get-factors nn try-factors) first-factor))
         :else (recur n remain))))
