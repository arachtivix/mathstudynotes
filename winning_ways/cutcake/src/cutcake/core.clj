(ns cutcake.core
  (:require [hiccup2.core :as h]
            [clojure.java.io :as io]))
; Lefty cuts north-south
; Rita cuts east-west
(def bootstrap-url "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css")
(def bootstrap-js "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js")

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
   (apply concat (single-move-results '() (first board) (rest board) player)))
  ([left-pile curr right-pile player]
   (if (nil? curr) '()
       (let [[w h] curr
             opts (cut-opts w h player)]
         (cons
          (map
           (fn [m] {:left left-pile :middle m :right right-pile})
           ;#(concat left-pile % right-pile)
           opts)
          (if (= 0 (count right-pile)) '()
              (single-move-results (concat left-pile (list curr))
                                   (first right-pile)
                                   (rest right-pile)
                                   player)))))))

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

(defn remove-ones
  [board]
  (filter #(not= [1 1] %) board))

; svg/html functions
(defn svg-rect
  [x y w h color]
  (h/html [:rect {:width w :height h :x x :y y :stroke "green"
                  :stroke-width 1 :fill color}]))

(defn cake-to-svg
  [rect-w rect-h cells-w cells-h color]
  (let [svg-w (* rect-w cells-w)
        svg-h (* rect-h cells-h)]
    (apply vector
           :svg
           {:width svg-w :height svg-h}
           (map
            (fn [[i j]]
              (svg-rect (* i rect-w) (* j rect-h) rect-w rect-h color))
            (for [i (range cells-w) j (range cells-h)] [i j])))))

(defn render-cake-list
  [ls rect-w rect-h color]
  (apply vector
         :span
         {:class "p-3"}
         (map
          (fn [[w h]]
            [:span {:class "p-1"} (cake-to-svg rect-w rect-h w h color)])
          ls)))

(defn calc-filename
  [board player]
  (let [simplified-board (remove-ones board)
        player-name (if (= player :RITA) "rita" "lefty")]
    (str (clojure.string/join "_" (flatten board))
         player-name ".html")))

(defn calc-filepath
  [board player]
  (let [filename (calc-filename board player)]
    (str "cutcake_pages/" filename)))

(defn render-opts
  [board player]
  (let [opts (single-move-results board player)
        other-player (if (= player :RITA) :LEFTY :RITA)]
    (apply vector :div
           (map
            (fn [{left :left
                  middle :middle
                  right :right}]
              [:div
               {:class "p-3"}
               [:a {:href (calc-filename (concat left middle right) other-player)}
                (render-cake-list left 20 20 "yellow")
                (render-cake-list middle 30 30 "orange")
                (render-cake-list right 20 20 "yellow")]])
            opts))))

(defn render-current-state
  [board player]
  [:div
   [:span player]
   [:div (render-cake-list board 50 50 "yellow")]
   [:div (render-opts board player)]])

(def bootstrap-css
  [:link {:rel "stylesheet" :href bootstrap-url}])

(def bootstrap-js
  [:script {:src bootstrap-js}])


(defn page-it
  [contents]
  (str (h/html [:html
                [:head
                 bootstrap-css
                 bootstrap-js
                 [:title "Cut Cake"]]
                [:body
                 {:style "text-align: center; background-color: #AACCFF"}
                 [:div
                  {:class "container"}
                  contents]]])))

(defn make-page
  [board player]
  (let [filepath (calc-filepath board player)
        file (io/file filepath)
        other-player (if (= player :RITA) :LEFTY :RITA)
        simplified-board (remove-ones board)]
    (if (not (.exists file))
        (do
          (spit filepath (page-it (render-current-state simplified-board player)))
          (let [children (single-move-results simplified-board player)]
            (for [c children] (make-page
                               (concat (:left c) (:middle c) (:right c))
                               other-player)))))))
