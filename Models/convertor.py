#!/usr/bin/env python3
import sys, pickle
from sklearn.tree import _tree

def print_tree_rules(tree, feature_names, class_names):
    tree_ = tree.tree_
    feature_name = [feature_names[i] if i != _tree.TREE_UNDEFINED else "undefined"
                    for i in tree_.feature]

    def recurse(node, rule):
        if tree_.feature[node] != _tree.TREE_UNDEFINED:
            name = feature_name[node]
            threshold = tree_.threshold[node]
            left_rule = f"{rule} & ({name} <= {threshold:.2f})" if rule else f"({name} <= {threshold:.2f})"
            recurse(tree_.children_left[node], left_rule)
            right_rule = f"{rule} & ({name} > {threshold:.2f})" if rule else f"({name} > {threshold:.2f})"
            recurse(tree_.children_right[node], right_rule)
        else:
            class_index = tree_.value[node].argmax()
            predicted_class = class_names[class_index]
            print(f"Rule: {rule} -> Predicted class: {predicted_class}")
    recurse(0, "")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 convertor.py <RF.pkl>")
        sys.exit(1)
    with open(sys.argv[1], 'rb') as f:
        model_rf = pickle.load(f)
    # Use provided feature names if available; else create dummy names
    feature_names = getattr(model_rf, "feature_names_in_", [f"f{i}" for i in range(model_rf.n_features_in_)])
    class_names = list(model_rf.classes_)
    for i, tree in enumerate(model_rf.estimators_):
        print(f"\nTree {i+1} rules:")
        print_tree_rules(tree, feature_names, class_names)

if __name__ == "__main__":
    main()
