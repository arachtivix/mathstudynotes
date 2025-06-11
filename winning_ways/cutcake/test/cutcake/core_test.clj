(ns cutcake.core-test
  #_{:clj-kondo/ignore [:refer-all]}
  (:require [clojure.test :refer :all]
            [cutcake.core :refer :all]))

(deftest lefty-split
  (testing "cut-opts splits for :LEFTY"
    (is (= (list (list [1 2] [1 2]))
           (cut-opts 2 2 :LEfty)))))

(deftest rita-split
  (testing "cut-opts splits for :RITA"
    (is (= (list (list [2 1] [2 1]))
           (cut-opts 2 2 :RITA)))))

