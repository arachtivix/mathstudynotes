(ns proj.p26.core-test
  (:require [clojure.test :refer :all]
            [proj.p26.core :refer :all]))

(deftest test-solve-1
  ;; bare minimum to hopefully preserve integrity between refactorings 
  (testing "Solution to Problem 26"
    (is (= 983 (solve-1 1000)))))