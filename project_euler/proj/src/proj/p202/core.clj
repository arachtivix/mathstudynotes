
(ns proj.p202.core
  (:gen-class))

;; Problem 202: Laserbeam
;; Created on 2025-06-23

(defn solve []
  ;; TODO: Implement solution
  nil)

(defn is-named-vertex? [[horiz vert]]
  (and (>= vert 0) (= (mod (abs horiz) 2) (mod (abs vert) 2)) (<= (abs horiz) (abs vert))))

(defn get-a-analogs
  ([depth-limit] (get-a-analogs depth-limit #{} [0 0]))
  ([depth-limit known-set [a b]]
   (cond (> (+ (abs a) b) depth-limit) known-set
         (some known-set [a b]) known-set
         :else (let [known-plus-cur (conj known-set [a b])
                     left-results (get-a-analogs depth-limit known-plus-cur [(- a 3) (+ b 3)])
                     up-results (get-a-analogs depth-limit left-results [a (+ b 2)])
                     right-results (get-a-analogs depth-limit up-results [(+ a 3) (+ b 3)])]
                 right-results))))

(defn -main []
  (println "Solution to Problem 202:")
  (println (solve)))
