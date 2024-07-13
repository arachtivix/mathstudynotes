(ns cutcake.core
  (:require [clojure.data.json :as json]
            [hiccup2.core :as h]))
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

(defn single-move-results
  ([board player]
   (single-move-results '() (first board) (rest board) player))
  ([left-pile curr right-pile player]
   (let [w (get curr 0)
         h (get curr 1)
         opts (cut-opts w h player)]
     (cons
      (map
       #(concat left-pile % right-pile)
       (cut-opts w h player))
      (if (= 0 (count right-pile)) '()
          (single-move-results (cons curr left-pile)
                               (first right-pile)
                               (rest right-pile)
                               player))))))
     

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
  ([w h]
  (cutcake w h {}))
  ([w h known]
  (cond (= w 1) (assoc known [w h] (* -1 (- h 1)))
        (= h 1) (assoc known [w h] (- w 1))
        :else (let [subs (reduce
                          (fn [cache [ww hh]]
                            (cutcake ww hh cache))
                          known
                          (get-unknown-pieces w h known))
                    l-best (eval-opts (cut-opts w h :LEFTY) subs :LEFTY)
                    r-best (eval-opts (cut-opts w h :RITA) subs :RITA)]
                (assoc subs [w h] (simplicity-rule l-best r-best))))))

; svg/html functions
(defn svg-rect
  [x y w h]
  (h/html [:rect {:width w :height h :x x :y y :stroke "green"
                  :stroke-width 1 :fill "yellow"}]))

(defn cake-to-svg
  [rect-w rect-h cells-w cells-h]
  (let [svg-w (* rect-w cells-w)
        svg-h (* rect-h cells-h)]
    (h/html [:svg {:width svg-w :height svg-h}
             (map
              (fn [[i j]]
                (svg-rect (* i rect-w) (* j rect-h) rect-w rect-h))
              (for [i (range cells-w) j (range cells-h)] [i j]))])))

(defn page-it
  [contents]
  (str (h/html [:html [:head [:title "an amazing page"]] [:body contents]])))
