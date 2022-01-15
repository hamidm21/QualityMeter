"""
Here we will use the listener generated by the listener to measure understandability.

"""

from qualitymeter.utils.walker_creator import WalkerCreator


class Understandability(WalkerCreator):
    def __init__(self, path):
        WalkerCreator.__init__(self, path)

    def calc_coupling(self):
        """
        calculating coupling.

        :return: average dcc
        """

        dcc = 0
        for c1 in self.classes:
            counted_once = []
            for c1_attr in c1.attribute:
                for c2 in self.classes:
                    if c2.identifier != c1.identifier and \
                            str(c2.identifier) in c1_attr.datatype and \
                            c1_attr.datatype not in counted_once:
                        dcc += 1
                        counted_once.append(c1_attr.datatype)
            for c1_method in c1.methods:
                for parameter_type in c1_method.parameters_type:
                    for c2 in self.classes:
                        if c2.identifier != c1.identifier and \
                                str(c2.identifier) in parameter_type and \
                                parameter_type not in counted_once:
                            dcc += 1
                            counted_once.append(parameter_type)

        return dcc / len(self.classes)

    def calc_cohesion(self):
        """
        calculating cohesion.

        :return: average cc
        """

        cc = 0
        for cls in self.classes:
            attributes_len = len(cls.attribute)
            methods_len = len(cls.methods)
            if attributes_len == 0 or methods_len == 0:
                continue
            invoked = {}
            for attr in cls.attribute:
                invoked[attr.identifier] = 0
            for method in cls.methods:
                counted_once = []
                for variable in method.variables:
                    for attr in cls.attribute:
                        if variable in str(attr.identifier) and variable not in counted_once:
                            invoked[attr.identifier] += 1
                            counted_once.append(str(attr.identifier))
            r = 0
            for item in invoked:
                r += invoked.get(item) / methods_len
            cc += r / attributes_len

        return cc / len(self.classes)

    def calc_design_size(self):
        """
        calculating design size.
        we want the count of all the classes in our project.

        :return: count of all the classes
        """

        result = 0
        for _ in self.classes:
            result += 1

        return result

    def calc_abstraction(self):
        """
        calculating abstraction.

        :return: results
        """

        list_of_ancestors = []
        for cls in self.classes:
            depth = 0
            temp = cls
            while len(temp.parents) != 0:
                depth += 1
                parent = self.find_parent(cls.parents[0])
                if len(parent) == 0:
                    break
                else:
                    temp = parent[0]
            list_of_ancestors.append(depth)

        if len(list_of_ancestors) != 0:
            result = sum(list_of_ancestors) / len(list_of_ancestors)
        else:
            result = 0

        return result

    def calc_encapsulation(self):
        """
        calculating encapsulation.

        :return: results
        """

        list_of_ratio = []
        for cls in self.classes:
            atr_count = 0
            atr_private_count = 0
            if len(cls.attribute) != 0:
                for atr in cls.attribute:
                    atr_count += 1
                    if "private" in atr.modifier or "protected" in atr.modifier:
                        atr_private_count += 1
                list_of_ratio.append(atr_private_count / atr_count)
            else:
                list_of_ratio.append(0)

        if len(list_of_ratio) != 0:
            result = sum(list_of_ratio) / len(list_of_ratio)
        else:
            result = 0

        return result

    def calc_polymorphism(self):
        """calculating polymorphism.

        Returns:
            (Int) result: the average number pf polymorphic methods in our project.
        """

        polymorphic_methods = []
        for cls in self.classes:
            polymorphic = 0
            if cls:
                for clmt in cls.methods:
                    if "private" not in clmt.modifiers and "final" not in clmt.modifiers and "static" not in clmt.modifiers:
                        polymorphic += 1
                polymorphic_methods.append(polymorphic)

        for inf in self.interfaces:
            polymorphic = 0
            if inf:
                for _ in inf.methods:
                    polymorphic += 1
                polymorphic_methods.append(polymorphic)

        if len(polymorphic_methods) != 0:
            result = sum(polymorphic_methods) / len(polymorphic_methods)
        else:
            result = 0

        return result

    def calc_complexity(self):
        """
        calculating complexity.

        :return: results
        """

        list_of_methods = []
        for cls in self.classes:
            list_of_methods.append(len(cls.methods))

        if len(list_of_methods) != 0:
            result = sum(list_of_methods) / len(list_of_methods)
        else:
            result = 0

        return result

    def get_value(self):
        """
        returning the final results along the Design Property metrics.

        :return: understandability, coupling, cohesion, design_size, abstraction, encapsulation, polymorphism,
        complexity
        """

        coupling = self.calc_coupling()
        cohesion = self.calc_cohesion()
        design_size = self.calc_design_size()
        abstraction = self.calc_abstraction()
        encapsulation = self.calc_encapsulation()
        polymorphism = self.calc_polymorphism()
        complexity = self.calc_complexity()

        understandability = -0.33 * abstraction + 0.33 * encapsulation - 0.33 * coupling + 0.33 * cohesion \
                            - 0.33 * polymorphism - 0.33 * complexity - 0.33 * design_size

        return understandability, coupling, cohesion, design_size, abstraction, encapsulation, polymorphism, complexity
