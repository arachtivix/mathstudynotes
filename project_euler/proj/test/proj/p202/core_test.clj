(ns proj.p202.core-test
  #_{:clj-kondo/ignore [:refer-all]}
  (:require [clojure.test :refer [deftest is testing]]
            [proj.p202.core :refer :all]))

(deftest is-named-vertex?-test
  (testing "Testing is-named-vertex?"
    (is (= true (is-named-vertex? [0 0])))
    (is (= true (is-named-vertex? [2 4])))
    (is (= true (is-named-vertex? [-2 4])))
    (is (= false (is-named-vertex? [0 1])))
    (is (= false (is-named-vertex? [2 -4])))
    (is (= false (is-named-vertex? [0 23])))
    (is (= false (is-named-vertex? [1 24])))
    (is (= false (is-named-vertex? [-5 0])))))

(deftest solve-test
  (testing "Testing solution"
    ;; TODO: Add test cases
    (is (= nil (solve)))))
