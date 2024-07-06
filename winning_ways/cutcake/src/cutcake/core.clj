(ns cutcake.core)

(symbol :LEFTY) ; Lefty cuts north-south
(symbol :RITA) ; Rita cuts east-west

; give the cuts possible, eliminating duplicates due to symmetry
(defn cut-opts
  ([w h]
   {:LEFTY (cut-opts w h :LEFTY)
    :RITA (cut-opts w h :RITA)})
  ([w h p]
  (cond (= p :LEFTY) (map
                     (fn [n] (list [(- w n) h] [n h]))
                     (range 1 (+ 1 (int (/ w 2)))))
        (= p :RITA) (map
                    (fn [n] (list [w (- h n)] [w n]))
                    (range 1 (+ 1 (int (/ h 2)))))
        :else (throw (Exception. "invalid player")))))

(defn eval-opt
  [opt cache]
  (reduce
   +
   (map #(get cache %) opt)))

(defn eval-opts
  [opts cache player]
  (reduce
   (if (= player :LEFTY) max min)
   (map #(eval-opt % cache) opts)))

(defn get-unknown-pieces
  [w h known]
  (let [opts (cut-opts w h)
        all-opts (concat (:RITA opts) (:LEFTY opts))]
    (set
     (filter #(nil? (get known %))
             (apply concat all-opts)))))

(defn simplicity-rule
  [l r]
  (cond (> l r) (throw (Exception. "l > r"))
        (= l r) 0
        (and (< l 0) (> r 0)) 0
        ;
        ; not checking for fractional cases, but here could be that
        ;
        (and (<= r 0) (<= l 0)) (- r 1)
        (and (>= r 0) (>= l 0)) (+ l 1)
        :else (throw (Exception. "not sure what happened"))))

(defn cutcake
  [w h known]
  (cond (= w 1) (assoc known [w h] (* -1 (- h 1)))
        (= h 1) (assoc known [w h] (- w 1))
        :else (let [subs (reduce
                          (fn [cache [ww hh]]
                            (cutcake ww hh cache))
                          known
                          (get-unknown-pieces w h known))
                    l-best (eval-opts (cut-opts w h :LEFTY) subs :LEFTY)
                    r-best (eval-opts (cut-opts w h :RITA) subs :RITA)]
                (assoc subs [w h] (simplicity-rule l-best r-best)))))

