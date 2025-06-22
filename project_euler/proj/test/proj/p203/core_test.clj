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

(deftest solve-test
  (testing "Testing solution"
    ;; TODO: Add test cases
    (is (= nil (solve)))))
