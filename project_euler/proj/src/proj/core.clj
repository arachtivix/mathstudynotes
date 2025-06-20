(ns proj.core
  #_{:clj-kondo/ignore [:unused-namespace]}
  (:require [proj.p3.core :as p3]
            [proj.p4.core :as p4]
            [proj.p7.core :as p7]
            [proj.p9.core :as p9]
            [proj.p10.core :as p10]
            [proj.p12.core :as p12]
            [proj.p15.core :as p15]
            [proj.p16.core :as p16]
            [proj.p26.core :as p26]
            [proj.p28.core :as p28]
            [proj.p51.core :as p51]
            [proj.p95.core :as p95]
            [proj.p205.core :as p205]
            [proj.p206.core :as p206]
            [proj.p361.core :as p361]
            [proj.p879.core :as p879]
            [clojure.math :as math]
            [proj.shared :as shared])
  (:gen-class))

(defn solve-problem
  "Solves the specified Project Euler problem"
  [problem-number]
  (case problem-number
    3 (p3/solve)
    4 (p4/solve)
    7 (p7/solve)
    9 (p9/solve)
    10 (p10/solve)
    12 (p12/solve)
    15 (p15/solve)
    16 (p16/solve)
    26 (p26/solve)
    28 (p28/solve)
    95 (p95/solve)
    361 (p361/solve)
    879 (p879/solve)
    (str "Problem " problem-number " not implemented yet")))

(defn -main
  "Main entry point - solves the specified problem or lists available problems"
  [& args]
  (if (empty? args)
    (println "Available problems: 3, 4, 7, 9, 10, 12, 15, 16, 26, 28, 95, 361, 879")
    (let [problem-number (Integer/parseInt (first args))]
      (println "Solution to Problem" problem-number ":")
      (println (solve-problem problem-number)))))
