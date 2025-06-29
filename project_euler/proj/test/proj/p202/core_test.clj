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

(deftest get-a-analogs-test
  (testing "Testing get-a-analogs"
    ;; worked these out using a drawing --- depth-limit-fn checks if sum of magnitudes > 8
    (is (= #{[0 0] [0 2] [3 3] [-3 3] [0 4] [0 6] [3 5] [-3 5] [0 8]} (get-a-analogs #(> (+ (abs %1) %2) 8))))
    ;; all the output from this function should be bona-fide named vertices
    (is (= true (reduce #(and %1 %2) (map is-named-vertex? (get-a-analogs #(> (+ (abs %1) %2) 20))))))))

(deftest solve-test
  (testing "Testing solution"
    ;; TODO: Add test cases
    (is (= nil (solve)))))
