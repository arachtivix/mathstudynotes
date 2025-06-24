(ns proj.p203.core-test
  #_{:clj-kondo/ignore [:refer-all]}
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p203.core :refer :all]))

(deftest next-pascal-row-test
  (testing "Testing next-pascal-row"
    (is (= [1 1] (next-pascal-row [1])))
    (is (= [1 2 1] (next-pascal-row [1 1])))
    (is (= [1 3 3 1] (next-pascal-row [1 2 1])))
    (is (= [1 4 6 4 1] (next-pascal-row [1 3 3 1])))))

(deftest pascal-seq-test
  (testing "Testing pascal-seq"
    (is (= '(1 1 1 1 2 1 1 3 3 1 1 4 6 4) (take 14 pascal-seq)))))

(deftest has-square-factor-test
  (testing "Testing has-square-factor"
    (is (= true (has-square-factor 4)))
    (is (= true (has-square-factor 75)))
    (is (= false (has-square-factor 5)))
    (is (= false (has-square-factor 13)))
    (is (= false (has-square-factor (* 13 7))))))

(deftest test-sol-1
  (testing "Testing solve-1"
    (is (= 105 (solve-1 8)))))