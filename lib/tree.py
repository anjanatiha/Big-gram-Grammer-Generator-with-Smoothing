import sys
import re


# removes multiple spaces with single space
def remove_multi_space(text):
	return re.sub(r' +', ' ', text)


class Node(object):
	def __init__(self, name=None, data=None, parent=None, size = 0):
		self.name = name
		self.data = data
		self.parent = parent
		self.children = []
		self.size = size

	def get_name(self):
		return self.name

	def set_data(self, data):
		self.data = data

	def get_data(self):
		return self.data

	def get_parent(self):
		return self.parent

	def add_child(self, child):
		self.children.append(child)
		child.parent = self
		self.size +=1

	def get_children(self):
		return self.children

	def get_first_child(self):
		return self.children[0]

	def get_last_child(self):
		return self.children[len(self.children)-1]

	def get_n_child(self, i):
		return self.children[i]


	def get_children_names(self):
		node_childrens = self.get_children()
		node_children_list_str = ""

		for child in node_childrens:
			node_children_list_str = node_children_list_str + child.get_name() + " "

		node_children_list_str = node_children_list_str.strip()

		return node_children_list_str


	def get_children_names_list(self):
		node_childrens = self.get_children()
		node_childrens_list = []

		for child in node_childrens:
			node_childrens_list.append(child.get_name())

		return node_childrens_list


	def remove_child(self, index):
		try:
			self.children.pop(index)
		except IndexError:
			print('Cannot remove. Child Index not found')

		return self.children


	def has_child(self):
		if len(self.children)>0:
			return 1
		else:
			return 0


	def get_sibblings(self):
		if self.parent is not None:
			parents_chidren = list(self.parent.children)
			parents_chidren.pop(self.get_index())
			siblings = parents_chidren

			return siblings

	def get_sibblings_names(self):
		if self.parent is not None:
			parents_chidren = list(self.parent.children)
			parents_chidren.pop(self.get_index())
			siblings = parents_chidren
			siblings_names = []

			for sibling in siblings:
				siblings_names.append(sibling.get_name())

			return siblings_names
	
	def get_index(self):
		for n, child in enumerate(self.parent.children):
			if child is self:
				return n

	def get_size(self):
		return self.size         
	
	def print_tree_original(self, rules=[], rules_map_full = {}, rules_map={}):
		rule = repr(self)
		rule = rule.strip()

		if rule != "":
			#print(rule)

			rule_right = rule.split(" -> ", 1)
			rule_right = rule_right[1]
			rule_right = "".join(rule_right)
			rule_right = remove_multi_space(rule_right)
			rule_right = rule_right.strip()
	
			if rule in rules_map_full:
				rules_map_full[rule] += 1
			else:
				rules_map_full[rule] = 1
				rules.append(rule)
	
	
			if rule_right in rules_map:
				rules_map[rule_right] += 1
				
			else:
				rules_map[rule_right] = 1
	

		if self.has_child() == 1:
			for child in self.get_children():
				child.print_tree(rules, rules_map_full, rules_map)

		return rules, rules_map_full, rules_map



	def print_tree(self, lexicalize, rules=[], rules_map_full = {}, rules_map={}):
		rule = ""
		rules_defined = ["NP", "VP"]
		if lexicalize == "":
			rule = repr(self)
		else:
			if len(self.get_children())>0 and self.get_data() != None and self.get_name() in rules_defined:
				children_names = ""
				children = self.get_children()
				for child in children:
					child_name = child.get_name()
					child_data = child.get_data()
					if child_data !=None:
						children_names = children_names + child.get_name() + "(" + child.get_data() + ")" + " "
					else:
						children_names = repr(self)
						break
				children_names = children_names.strip()

				rule = self.get_name() + "(" + self.get_data() + ")" + " -> " + children_names
			else:
				rule = repr(self)

		
		rule = rule.strip()

		if rule != "":
			#print(rule)

			rule_right = rule.split(" -> ", 1)
			rule_right = rule_right[1]
			rule_right = "".join(rule_right)
			rule_right = remove_multi_space(rule_right)
			rule_right = rule_right.strip()
	
			if rule in rules_map_full:
				
				rules_map_full[rule] += 1
				
			else:
				rules_map_full[rule] = 1
				rules.append(rule)
	
	
			if rule_right in rules_map:
				rules_map[rule_right] += 1
				
			else:
				rules_map[rule_right] = 1
	

		if self.has_child() == 1:
			for child in self.get_children():
				child.print_tree(lexicalize, rules, rules_map_full, rules_map)

		return rules, rules_map_full, rules_map


	def __repr__(self):
		if len(self.get_children())>0:
			return self.get_name() + " -> " + self.get_children_names()
		else:
			return ""

	def print_tree_all(self, level=0):
		print('\t' * level + '+'*(level+1) + repr(self))
		# Check if in infinite recursion loop.
		for child in self.children:
			child.print_tree_all(level+1)

	'''
	# for full tree
	def __repr__(self):
		return '[Node:{0}|Parent:{1}]'.format(self.name, self.parent)
	'''
	
	
	def get_children_list_grammer(self):
		node_childrens = self.get_children()
		node_children_list = []
		node_children_list_str = str(self.get_name()) + " ->"

		for child in node_childrens:
			node_children_list.append(child.get_name())
			node_children_list_str = node_children_list_str + " " + child.get_name()


		return node_childrens, node_children_list, node_children_list_str

	def choose_head(self, node_type):
		children = []
		children_names = []
		parent = ""
		parent_name = ""

		if node_type=="leaf":
			children = self.get_sibblings()
			parent = self.get_parent()
			parent_name = parent.get_name()
		else:
			children = self.get_children()
			children_names = []
			parent = self
			parent_name = parent.get_name()

		for child in children:
			children_names.append(child.get_data())

		chosen = ""
		children_len = len(children)

		if parent_name == "NP":
			if bool(set(children_names) & set(["NN", "NNS", "NNP"])):
				for i in range(children_len-1, -1, -1):
					if children_names[i] in ["NN", "NNS", "NNP"]:
						chosen = children[i].get_data()
						
						break

				#print("NP-------")	
			
			elif "NP" in children_names:
				for i in range(children_len):
					if children_names[i] == "NP":
						chosen = children[i].get_data()
						break
					i +=1
				#print("NP-------")

			elif "JJ" in children_names:
				for i in range(children_len-1, -1, -1):
					if children_names[i] == "JJ":
						chosen = children[i].get_data()
						break
					#i -= 1
				#print("NP-------")

			elif "CD" in children_names:
				for i in range(children_len-1, -1, -1):
					if children_names[i] == "CD":
						chosen = children[i].get_data()
						break
					#i -= 1
				#print("NP-------")
			else:
				if len(children)>0:
					chosen = children[len(children)-1].get_data()
		

		elif parent_name == "VP":
			children_len = len(children)

			if bool(set(children_names) & set(["VI", "VT"])):
				for i in range(children_len):
					if children_names[i] in ["VI", "VT"]:
						chosen = children[i].get_data()
						break
					i += 1

			elif "VP" in children_names:
				for i in range(children_len):
					if children_names[i] == "VP":
						chosen = children[i].get_data()
						break
					i +=1
			else:
				if children_len > 0:
					chosen = children[0].get_data()
		
		if node_type=="leaf":
			self.parent.set_data(chosen)
		else:
			self.set_data(chosen)
		
		return chosen


	def lexicalize_data(self):

		if self.data != None:
			if self.parent == None:
				return
			else:
				if self.parent.data == None:
					self.parent.lexicalize_data()
				else:
					return 
		else:
			if len(self.get_children()) > 0:

				children = self.get_children()
				for child in children:
					
					if child.data == None:
						child.lexicalize_data()
					else:
						if len(child.get_children()) == 0:
							child.choose_head("leaf")
						else:
							child.lexicalize_data()

				self.choose_head("")
			else:
				self.choose_head("leaf")

		

'''

root = Node(name='NP')
child1 = Node(name='NP')
child2 = Node(name='VP')
child3 = Node(name='NP')
child4 = Node(name='NP')
child5 = Node(name='child5')
child6 = Node(name='child6')
child7 = Node(name='child7')
child8 = Node(name='child8')


child5.set_data("VP")
child6.set_data("VI")

child7.set_data("NN")
child8.set_data("NNP")

root.add_child(child1)
root.add_child(child2)
child1.add_child(child3)
child1.add_child(child4)
child2.add_child(child5)
child2.add_child(child6)
child3.add_child(child7)
child3.add_child(child8)

root.lexicalize_data()
print("data: ", child1.get_name(), child1.get_data())
print("data: ", root.get_name(), root.get_data())
print("data: ", child2.get_name(), child2.get_data())
print("data: ", child3.get_name(), child3.get_data())
print("data: ", child4.get_name(), child4.get_data())
print("data: ", child5.get_name(), child5.get_data())
print("data: ", child6.get_name(), child6.get_data())
print("data: ", child7.get_name(), child7.get_data())
print("data: ", child8.get_name(), child8.get_data())

root.print_tree("lex")
'''
