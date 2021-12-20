"""
DO NOT MODIFY ANY GIVEN FIELDS OR FUNCTIONS 
"""

class JoinGraph:
    """
    A class used to represent a join graph

    Fields
    -----------
    relations : [Relation]
        all join relations specified in the input file
    joinConditions : [JoinCondition]
        all join conditions specified in the input file
    """

    relations = None
    joinConditions = None
    
    def __init__(self, path : str) -> None:
        with open(path, "r") as f:
            lines = f.readlines()
            self._load(lines)
    
    def getBestJoinOrder(self):
        n = len(self.relations)
        S = [[None for j in range(0, n)] for i in range(0, n)]
        for i in range(n):
            S[i][i] = JoinPlan(None, None, [self.relations[i]], self.relations[i].cardinality)
        for i in range(n-1):
            if self.relations[i+1].cardinality < self.relations[i].cardinality:
                left = i+1
                right = i
            else:
                left = i
                right = i+1
            lst = [self.relations[left], self.relations[right]]
            S[i][i+1] = JoinPlan(S[left][left], S[right][right], lst, self._getCardinality(lst))
        for numRels in range(3, n+1):
            i = 0
            while i < n-numRels+1:
                j = i + numRels - 1
                Tk = -1
                for k in range(i, j):
                    if S[i][k].estOutCard < S[k+1][j].estOutCard:
                        left = S[i][k]
                        right = S[k+1][j]
                    else:
                        right = S[i][k]
                        left = S[k+1][j]
                    loR = left.relations + right.relations
                    newPlan = JoinPlan(left, right, loR, self._getCardinality(loR))
                    if Tk > newPlan.estCost or Tk == -1:
                        S[i][j] = newPlan
                        Tk = newPlan.estCost
                i += 1
        return S[0][n-1]

    def _load(self, lines : list) -> None:
        """
        Inject join relations and conditions
        """
        assert(len(lines) >= 3)
        numRelations = int(lines[0])
        self.relations = [None] * numRelations
        # inject join relations
        cardinalities = lines[1].split(",")
        assert(len(cardinalities) == numRelations)
        relationNameIdxMap = {}
        for i in range(numRelations):
            relationName = "R" + str(i)
            self.relations[i] = Relation(relationName, i, int(cardinalities[i]))
            relationNameIdxMap[relationName] = i
        # inject foreign keys
        foreignRelationNames = lines[2].split(",")
        assert(len(foreignRelationNames) == numRelations - 1)
        self.joinConditions = [None] * (numRelations - 1)
        for i in range(numRelations - 1):
            foreignRelationIdx = relationNameIdxMap[foreignRelationNames[i]]
            if i == foreignRelationIdx:
                self.joinConditions[i] = JoinCondition(self.relations[i+1], self.relations[i])
            elif i + 1 == foreignRelationIdx:
                self.joinConditions[i] = JoinCondition(self.relations[i], self.relations[i+1])
            else:
                assert(False)

    def _getCardinality(self, inRelations : list) -> int:
        """
        Compute cardinality given a list of join relations
        Input: [Relation]
        Output: int
            estimated output cardinality of given join relations
        """
        assert(len(inRelations) >= 2)
        inRelations.sort(key = lambda x : x.idx)
        cardinality = inRelations[0].cardinality
        for i in range(1, len(inRelations)):
            cardinality *= inRelations[i].cardinality
            if inRelations[i - 1].idx + 1 == inRelations[i].idx:
                joinCondition = self.joinConditions[inRelations[i - 1].idx]
                cardinality /= joinCondition.foreignRelation.cardinality
            else:
                print("[Warning] Estimating join relations containing Cartesian Product.")
        return cardinality

class Relation:
    """
    A class used to represent base relation table
    
    Fields
    -----------
    name : str
        name of the relation
    idx  : int
        index of the relation generated during injection
    cardinality : int
        cardinality of the relation
    """

    name = None
    idx = None
    cardinality = None

    def __init__(self, name : str, idx : int, cardinality : int) -> None:
        self.name = name
        self.idx = idx
        self.cardinality = cardinality
    
    def __str__(self) -> str:
        """
        Represent relation in the format of name(idx):cardinality
        E.g. A(0):50
        """
        return self.name + "(" + str(self.idx) + "):" + str(self.cardinality)

class JoinCondition:
    """
    A class used to track foreign key for chain joins

    Fields
    -----------
    primaryRelation : Relation
        relation containing primary key
    foreignRelation : int
        relation containing foreign key
    """
    
    primaryRelation = None
    foreignRelation = None
    
    def __init__(self, primaryRelation : Relation, foreignRelation : Relation) -> None:
        self.primaryRelation = primaryRelation
        self.foreignRelation = foreignRelation

class JoinPlan:
    """
    A class used to represent a logical join tree

    Fields
    -----------
    left : JoinPlan
        left child
    right : JoinPlan
        right child
    relations : [Relation]
        join relations matched in the join tree
    estOutCard : int
        estimated output cardinality of the join tree
    estCost : int
        cost of the join tree
    """
    
    left = None
    right = None
    relations = None
    estOutCard = 0
    estCost = 0

    def __init__(self, left, right, relations : list, estOutCard : int) -> None:
        self.left = left
        self.right = right
        self.relations = relations
        self.estOutCard = int(estOutCard)
        if self.isLeaf():
            self.estCost = 0
        else:
            self.estCost = left.estCost + right.estCost + self.estOutCard

    def isLeaf(self) -> bool:
        """
        Check if this is the leaf
        """
        return self.left is None and self.right is None
    