# -*- coding: utf-8 -*-

import numpy as np
from random import shuffle

def svm_loss_naive(W, X, y, reg):
    """
    Structureed SVM loss function, naive implementation (with loops).
    
    Inputs:
    - W: C x D array of weights
    - X: D x N array of data. Data are D-dimensional colun vetors
    - y: 1-dimensional array of length N with labels 0...K-1, for K classes
    - reg: (float) regularization strength
    
    Returns:
    a tuple of :
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    dW = np.zeros(W.shape)  # initialize the gradient as zero
    
    # compute the loss and the gradient
    num_classes = W.shape[0]
    num_train = X.shape[1]
    loss = 0.0
    delta = 1
    for i in range(num_train):
        scores = W.dot(X[:,i])
        correct_class_score = scores[y[i]]
        for j in range(num_classes):
            if j == y[i]:   # if correct class
                continue
            margin = scores[j]-correct_class_score+delta
            if margin > 0: 
                loss += margin
                # dW_j = partial(loss)/partial(w_j) = X_i.T
                # dW_y = partial(loss)/partial(w_y) = -X_i.T
                # Compute dW_j and dW_y simulataneously
                dW[j,:] += X[:,i].T      
                dW[y[i],:] -= X[:,i].T
            
    # Right now the loss is a sum over all training examples, but we want it 
    # to be an average instead so we divide by num_train
    loss /= num_train

    # Avarage gradients as well
    dW /= num_train

    # Add regularization to the loss
    loss += 0.5 * reg * np.sum(W * W) # W * W like the dot product in Matlab

    # Add regularization to the gradient
    dW += reg * W

    #############################################################################
    # TODO                                                                      #
    # Compute the gradient of the loss function and store it dW.                #
    # Rather than first computing the loss and then computing the derivative,   #
    # it may be simplier to compute the derivative at the same time that the    #
    # loss is being computed. A s a result you may need to modify some of the   #
    # code above to compute the gradient.                                       #
    #############################################################################

    return loss, dW
def svm_loss_vectorized(W, X, y, reg):
    """
    Structured SVM loss function, vectorized implementation.
    Inputs and returns are the same as svm_loss_naive.
    """
    loss = 0.0
    dW = np.zeros(W.shape)  # initialize the gradient as zero
    #############################################################################
    # TODO                                                                      #
    # Implement a vectorized version of structured SVM loss, storing the result #
    # in loss.                                                                  #
    #############################################################################
    scores = np.dot(W, X) # also known as f(x_i, W), D x N dimension
        
    correct_scores = np.ones(scores.shape) * scores[y, np.arange(0, scores.shape[1])]
    # correct_scores is a D x N dimensional array, each element in the same column
    # is same.

    deltas = np.ones(scores.shape)
    L = scores - correct_scores + deltas

    L[L < 0] = 0
    L[y, np.arange(0, scores.shape[1])] = 0 # do not count y_i
    loss = np.sum(L)

    # Average over number of training examples
    num_train = X.shape[1]
    loss /= num_train

    # Add regularization 
    loss += 0.5 * reg * np.sum(W * W)

    #############################################################################
    # TODO                                                                      #
    # Implement a vectorized version of the gradient for the structured SVM     #
    # loss, storing the result in dW.                                           #
    # Hint:
    # Instead of computing the gradient from scratch, it may be easier to reuse #
    # some of the intermediate values that you used to compute the loss.        #
    #############################################################################
    L = scores - correct_scores + deltas   # (K x N) dimension

    L[L < 0] = 0
    L[L > 0] = 1
    L[y, np.arange(0, scores.shape[1])] = 0     # do not count y_i
        
    L[y, np.arange(0, scores.shape[1])] = -1 * np.sum(L, axis = 0) 
    # Note:
    #     S_y计入loss的个数是np.sum(L, axis = 0)
    dW = np.dot(L, X.T)

    dW /= num_train

    return loss, dW