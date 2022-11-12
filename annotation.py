from treelib import Tree
import re

class Annotation:

    def __int__(self):
        pass

    def buildQueryTree(self, plan_list, tree=None, parent=None):

        if tree is None:
            tree = Tree()

        for plan in plan_list:

            if parent is None:
                node = tree.create_node(tag=plan['Node Type'], data=plan)
            else:
                node = tree.create_node(
                    tag=plan['Node Type'], data=plan, parent=parent.identifier)

            if "Plans" in plan:
                self.buildQueryTree(plan["Plans"], tree, node)

        return tree

    def annotate(self, tree, inputquery):
        result_dict = {}
        nodeList = tree.all_nodes()

        for node in nodeList:

            explanation = ""
            if node.tag == "Seq Scan":
                tableName = node.data["Relation Name"]
                totalCost = node.data["Total Cost"]

                explanation += "{} table is read using sequential scan. This is because no index is created in the table.\n".format(
                    tableName)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Index Scan":
                tableName = node.data["Relation Name"]
                indexName = node.data["Index Name"]
                totalCost = node.data["Total Cost"]

                explanation += "{} table is read using index scan. This is because index {} is created in the table.\n".format(
                    tableName, indexName)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Index Only Scan":
                tableName = node.data["Relation Name"]
                indexName = node.data["Index Name"]
                totalCost = node.data["Total Cost"]

                explanation += "{} table is read using index only scan. This is because index {} is created in the table.\n".format(
                    tableName, indexName)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Bitmap Heap Scan":
                tableName = node.data["Relation Name"]
                joinCond = node.data["Recheck Cond"]
                totalCost = node.data["Total Cost"]

                explanation += "{} table is read using bitmap heap scan with the join condition {}.\n".format(
                    tableName, joinCond)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Bitmap Index Scan":
                indexName = node.data["Index Name"]
                joinCond = node.data["Index Cond"]
                totalCost = node.data["Total Cost"]
                tableName = indexName.split('_')[0]

                explanation += "{} table is read using bitmap heap scan with the join condition {}. This is because index {} is created in the table. \n".format(
                    tableName, joinCond, indexName)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Hash Join":
                joinCond = node.data["Hash Cond"]
                totalCost = node.data["Total Cost"]

                explanation += "This join is implemented using hash join operator with the join condition {}.\n".format(
                    joinCond)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Merge Join":
                joinCond = node.data["Merge Cond"]
                totalCost = node.data["Total Cost"]

                explanation += "This join is implemented using merge join operator with the join condition {}.\n".format(
                    joinCond)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Nested Loop":
                totalCost = node.data["Total Cost"]

                explanation += "This join is implemented using nested loop inner join operator.\n"
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Sort":
                totalCost = node.data["Total Cost"]
                sortKey = node.data["Sort Key"]

                explanation += "The sort by using sort key {}.\n".format(
                    sortKey)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Incremental Sort":
                totalCost = node.data["Total Cost"]
                sortKey = node.data["Sort Key"]

                explanation += "Incremental sort is performed with the sort key {}.\n".format(
                    sortKey)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Hash":
                totalCost = node.data["Total Cost"]
                hashBucket = node.data["Hash Buckets"]

                explanation += "The hash into {} hash buckets.\n".format(
                    hashBucket)
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Aggregate":
                totalCost = node.data["Total Cost"]

                if 'Group Key' in node.data:
                    groupKey = node.data["Group Key"]

                    explanation += "Aggregate is performed with the group key {}.\n".format(
                        groupKey)
                    explanation += "Total cost is {}".format(totalCost)
                else:
                    explanation += "Aggregate is performed.\n"
                    explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Gather Merge":
                totalCost = node.data["Total Cost"]

                explanation += "Gather Merge is performed.\n"
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Gather":
                totalCost = node.data["Total Cost"]

                explanation += "Gather is performed.\n"
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Limit":
                totalCost = node.data["Total Cost"]

                explanation += "Limit is performed.\n"
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Memoize":
                totalCost = node.data["Total Cost"]

                explanation += "Memoize is performed.\n"
                explanation += "Total cost is {}".format(totalCost)

            elif node.tag == "Materialize":
                totalCost = node.data["Total Cost"]

                explanation += "Materialize is performed.\n"
                explanation += "Total cost is {}".format(totalCost)

            result_dict[node.identifier] = explanation

        return result_dict

    def matchNodeToQuery(self, tree, inputquery):
        inputquery = inputquery.lower()
        result_dict = {}
        nodeList = tree.all_nodes()
        regex = re.compile('[^a-zA-Z._]')
        for node in nodeList:
            pos = []

            if node.tag == "Seq Scan" or node.tag == "Index Scan":
                toHighlight = node.data['Relation Name']
                for match in re.finditer(toHighlight, inputquery):
                    pos.append((match.start(), match.end()))

                if node.identifier in result_dict:
                    result_dict[node.identifier] = result_dict[node.identifier] + pos
                else:
                    result_dict[node.identifier] = pos

            elif node.tag == "Hash Join":
                toHighlight = node.data['Hash Cond']
                if '=' in toHighlight:
                    toHighlightList = []
                    toHighlightList.append('=')
                    elems = toHighlight.split('=')
                    toHighlightList.append(regex.sub('', elems[0]))
                    toHighlightList.append(regex.sub('', elems[1]))

                    for elem in toHighlightList:
                        for match in re.finditer(elem, inputquery):
                            pos.append((match.start(), match.end()))

                    result_dict[node.identifier] = pos

                else:
                    for match in re.finditer(toHighlight, inputquery):
                        pos.append((match.start(), match.end()))

                    result_dict[node.identifier] = pos

            elif node.tag == "Merge Join":
                toHighlight = node.data['Merge Cond']
                if '=' in toHighlight:
                    toHighlightList = []
                    toHighlightList.append('=')
                    elems = toHighlight.split('=')
                    toHighlightList.append(regex.sub('', elems[0]))
                    toHighlightList.append(regex.sub('', elems[1]))

                    for elem in toHighlightList:
                        for match in re.finditer(elem, inputquery):
                            pos.append((match.start(), match.end()))

                    result_dict[node.identifier] = pos

                else:
                    for match in re.finditer(toHighlight, inputquery):
                        pos.append((match.start(), match.end()))

                    result_dict[node.identifier] = pos

            elif node.tag == "Aggregate":
                # return list
                if 'Group Key' in node.data:
                    toHighlightList = node.data['Group Key']

                    for elems in toHighlightList:
                        # {customer.c_custkey, nation.n_name}
                        for elem in elems.split('.'):
                            elem = elem.replace('(','').replace(')','')
                            for match in re.finditer(elem, inputquery):
                                pos.append((match.start(), match.end()))
                                break

                            if node.identifier in result_dict:
                                result_dict[node.identifier] = result_dict[node.identifier] + pos
                            else:
                                result_dict[node.identifier] = pos

        return result_dict
