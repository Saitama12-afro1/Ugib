class Solution:
    def removeComments(self, source):
        stack = []
        answer = []
        for i, val in enumerate(source):
            
            if "/*" in val and "*/" not in val:
                buff = val.split("/*")[0]
                if buff:
                    answer.append(buff)
                stack.append(i)
                continue
            elif "/*" not in val and "*/" in val:
                buff = answer[len(answer) - 1] + val.split("*/")[1]
                if buff:
                    answer[len(answer) - 1] = buff
                stack.pop(buff)
                continue
            elif "/*"  in val and "*/" in val:
                print(val)
                buff = val.split("/*")[0] + val.split("/*")[1].split("*/")[1]
                if buff:
                    answer.append()
                continue
            elif "//" in val:
                answer.append(val.split("//")[0])
                continue
            if stack:
                continue
            else:
                answer.append(val)
        return answer
source = ["struct Node{", "    /*/ declare members;/**/", "    int size;", "    /**/int val;", "};"]
Solution.removeComments(None,source)



