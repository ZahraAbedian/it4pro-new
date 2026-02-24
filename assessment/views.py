from django.shortcuts import render
from .models import Answers
from .models import Questions
from .models import Categories
from .models import Paragraphs  
from .models import UserAnswers
from .models import UserCategories
from .models import UserResult
from mauth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.conf import settings
from .utils import drawRadarChart, chechAndDrawResults, getListOfTask
from mauth.models import myprofile
import random, string
# calculate score for each category per user 
def calculateScores(uid):
        myCategories = Categories.objects.all()
        for mca in myCategories:
                catScore = 0
                myQuestions = Questions.objects.filter(question_fk=mca)
                point = 5/len(myQuestions)
                for mqu in myQuestions:
                        userAnswerId = UserAnswers.objects.filter(user = uid, question = mqu).first().answer.id
                        if(userAnswerId==1):
                                catScore += point
                        if(userAnswerId==2):
                                catScore += (point/2)
                UserCategories.objects.update_or_create(
                                        user = uid,
                                        category = mca,
                                        defaults={"score" : round(catScore)}
                                )

# check and update user us is completed all questions in ca category or not
# this function return true if all questions in ca is answered by user us
# also set UserCategories dataset if all questions in ca is answered by user us
def checkSetCategoryComp(us, ca):
        cate = Categories.objects.filter(category_order=ca).first()
        
        questions_ca= Questions.objects.filter(question_fk__category_order=ca)
        answeredAllCaQuestions = True
        for i in questions_ca:
                userAnswers = UserAnswers.objects.filter(user = us, question = i)
                if(len(userAnswers) > 0):
                        pass
                else:
                        answeredAllCaQuestions = False
                        break
        if(answeredAllCaQuestions):
                if(len(UserCategories.objects.filter(user=us, category=cate)) == 0):
                        uc = UserCategories(user=us, category=cate)
                        uc.save()
        else:
                if(len(UserCategories.objects.filter(user=us, category=cate)) != 0):
                        UserCategories.objects.filter(user=us, category=cate).delete()
        return answeredAllCaQuestions


# this function check for all category compeletion for uid user
# return true if all categories is answered by user
def checkAllQuestionsIsAnswered(uid, lockQuestions):
        ur = UserResult.objects.filter(user=uid)
        allCategoriesIsComplete = True
        if(len(ur)!=0):
                return ur.first().QuestionLock
        else:
                categories_views = Categories.objects.all()
                for cat in categories_views:
                        if(not checkSetCategoryComp(uid, cat.category_order)):
                                allCategoriesIsComplete = False
                if(lockQuestions and allCategoriesIsComplete):
                        radarChartName = ''.join(random.choices(string.ascii_letters+string.digits, k=20)) + '.png'
                        barChartName = ''.join(random.choices(string.ascii_letters+string.digits, k=20)) + '.png'
                        UserResult(user=uid, radarChart=radarChartName, barChart=barChartName, QuestionLock=True, Change=True).save()
        return allCategoriesIsComplete
        

# final Score
# uid is user object
def finalScore(uid):
        allUserCategories = UserCategories.objects.filter(user=uid)
        finalScore = 0
        for usca in allUserCategories:
                finalScore += usca.score
        return(round(finalScore/len(allUserCategories)))
# Create your views here.

# questionPageContent = {0: {"img":'assessment/banner/main-Banner.jpg',
#                               "heading":"ITSM Process Maturity Question sets",
#                               "paras":["1.Begin your journey by selecting the Question Sets. You will be presented with all available Question Sets for your assessment.",
#                                        "2.Each Question Set pertains to a specific ITSM process, and all sets will be displayed when you initiate your journey.",
#                                        "3.Your ITSM Maturity Level will be displayed upon the completion of your responses.",
#                                        "4.To revisit your ITSM Maturity Level, please select the Report Dashboard, where you will have access to your report."]
#                              },
#                        1: {"img":'assessment/banner/availability-Banner.jpg',
#                               "heading":"Availability Management",
#                               "paras":["1.You will be presented with all available Question Sets for your assessment.",
#                                        "2.TSM process, and all sets will be displayed when you initiate your journey.",
#                                        "3.ed upon the completion of your responses.",
#                                        "4.ase select the Report Dashboard, where you will have access to your report."]
#                              }
#                         }



# questionPageContent = {0: {"img":'assessment/banner/main-Banner.jpg',
#                               "heading":"ITSM Process Maturity Question sets",
#                               "paras":["1.Begin your journey by selecting the Question Sets. You will be presented with all available Question Sets for your assessment.",
#                                        "2.Each Question Set pertains to a specific ITSM process, and all sets will be displayed when you initiate your journey.",
#                                        "3.Your ITSM Maturity Level will be displayed upon the completion of your responses.",
#                                        "4.To revisit your ITSM Maturity Level, please select the Report Dashboard, where you will have access to your report."]
#                              }}

@login_required(login_url= '/auth/login')
def mainPage(request):
        return render(request, "assessment/mainPage.html") 



# def questionsPage(request):
#         getOrder = request.GET.get('cod', '-1')
#         currentCategoryOrder = 0
#         if(int(getOrder) >= 0):
#                 currentCategoryOrder = int(getOrder)

#         answers_views = Answers.objects.all()
#         questions_views = Questions.objects.filter(question_fk__category_order=getOrder).order_by('question_order')
#         categories_views = Categories.objects.all()
#         content = questionPageContent[currentCategoryOrder]
#         return render(request, "assessment/questionsPage.html", {"cco":currentCategoryOrder,"content":content, "answers": answers_views, "questions": questions_views, "categories": categories_views}) 


@login_required(login_url= '/auth/login')
def questionsPage(request):
        
        uid = User.objects.get(id=request.user.id)

        if(len(UserResult.objects.filter(user=uid))!=0):
                if(UserResult.objects.filter(user=uid).first().QuestionLock):
                        return render(request, "assessment/messagePage.html", {
                                "headingMessage":"You have answered to all questions.",
                                "paragraphMessage":"Please see report dashboard",
                                "activeSide":"questionSets"})


        # Write or update the answer sent by the user 
        listOfAnswered = []
        if request.method == "POST":
                for qid,aid in request.POST.items():
                        listOfAnswered.append(qid)
                        if(qid!="csrfmiddlewaretoken"):
                                qs = Questions.objects.get(id=qid)
                                anws = Answers.objects.get(id=aid)
                                UserAnswers.objects.update_or_create(
                                        user = uid,
                                        question = qs,
                                        defaults={"answer" : anws}
                                )
        
        # Because the user can move between the categories in two directions, 
        # previous category order (pcod) variable is used to check the completion of the questions of that category.
        pcod = request.GET.get('pcod', '-1')
        if (int(pcod) > 0):
                checkSetCategoryComp(uid, int(pcod))
        
        # list of compeleted categories by user
        completedCategories = UserCategories.objects.filter(user=uid)
        completedCategoriesList=[]
        for ccat in completedCategories:
                completedCategoriesList.append(ccat.category.category_order)


        # current category order (cod)
        getOrder = request.GET.get('cod', '-1')
        currentCategoryOrder = 0
        if(int(getOrder) >= 0):
                currentCategoryOrder = int(getOrder)

        #set max seen category order
        mcod = int(request.GET.get('mcod', '0'))
        if(mcod < currentCategoryOrder):
                mcod = currentCategoryOrder


        # prepare questions(related to cod), answers, categories for front template
        answers_views = Answers.objects.all()
        questions_views = Questions.objects.filter(question_fk__category_order=getOrder).order_by('question_order')
        categories_views = Categories.objects.all()

        # get current category object
        current_category = Categories.objects.filter(category_order=getOrder).first()
        
        # get list of Question, Answer (listOfQA), where answered by user to show on front template
        listOfQA={}
        for i in questions_views:
                userAnswers = UserAnswers.objects.filter(user = uid, question = i)
                if(len(userAnswers) > 0):
                        listOfQA[i.id]=userAnswers.first().answer.id
        

        # prepare photo, heading, paragraphs for top of page for each category
        paragraph_views = None
        photo_value = None
        heading_value = "" 
        if current_category:  
                paragraph_views = Paragraphs.objects.filter(paragraph_fk = current_category)
                photo_value = '/'.join(current_category.photo.url.split('/')[3:])
                heading_value = current_category.heading
        
        # all questions is answered (aqia) to show result page or not
        aqia = 0
        if currentCategoryOrder > len(categories_views):
                aqia = int(checkAllQuestionsIsAnswered(uid, False))
                currentCategoryOrder = -1 
        

        return render(request, "assessment/questionsPage.html", {"cco": currentCategoryOrder,
                                                                 "mcod":mcod,
                                                                 "aqia":aqia,
                                                                 "photo": photo_value, 
                                                                 "heading": heading_value, 
                                                                 "paragraphs": paragraph_views, 
                                                                 "answers": answers_views, 
                                                                 "questions": questions_views, 
                                                                 "categories": categories_views,
                                                                 "listOfQA": listOfQA,
                                                                 "completedCategories":completedCategoriesList,
                                                                 "activeSide":"questionSets"}) 


@login_required(login_url= '/auth/login')
def resultPage(request):
        uid = User.objects.get(id=request.user.id)
        if(checkAllQuestionsIsAnswered(uid, True)):
                calculateScores(uid)
                data, cats, statusImage, radarChartName, barChartName, ResultPageDownContent = chechAndDrawResults(uid)
                finalScoreImg = "assessment/result/management"+str(finalScore(uid))+".jpg"
                return render(request, "assessment/resultPage.html", 
                {"fsi":finalScoreImg, 
                 "activeSide":"reportDashboard",
                 "statusImage":statusImage,
                 "radarChartName":radarChartName,
                 "barChartName":barChartName,
                 "categories":cats,
                 "RPDC": ResultPageDownContent
                 })
        else:
                return render(request, "assessment/messagePage.html", {
                                "headingMessage":"You have some unanswered questions.",
                                "paragraphMessage":"Please see question stes",
                                "activeSide":"reportDashboard"})
                

@login_required(login_url= '/auth/login')
def taskPage(request):
        uid = User.objects.get(id=request.user.id)
        if(not checkAllQuestionsIsAnswered(uid, False)):
                return render(request, "assessment/messagePage.html", {
                                "headingMessage":"You have some unanswered questions.",
                                "paragraphMessage":"Please see question stes"})
        catId=-1
        try:
                catId = int(request.GET.get('catId', '-1'))
        except:
                catId=-1
        categories = Categories.objects.all()
        if catId == -1:
                catId = categories.first().id
        # if catId != -1:
        #         selectCat
        #         photo = '/'.join(ucs.category.photo.url.split('/')[3:])
        selectedCat = Categories.objects.filter(id=catId).first()
        tasksDic = getListOfTask(selectedCat, uid)
        someThingsChanged = False
        if request.method == "POST":
                if(catId != -1):
                        for mqt in Questions.objects.filter(question_fk = selectedCat):
                                if(request.POST.get(str(mqt.id)) and (not tasksDic[mqt.id][0])):
                                        UserAnswers.objects.update_or_create(
                                        user = uid,
                                        question = mqt,
                                        defaults={"answer" : Answers.objects.get(id=1)}
                                        )
                                        someThingsChanged = True
                                if((not request.POST.get(str(mqt.id))) and tasksDic[mqt.id][0]):
                                        UserAnswers.objects.update_or_create(
                                        user = uid,
                                        question = mqt,
                                        defaults={"answer" : Answers.objects.get(id=3)}
                                        )
                                        someThingsChanged = True

        tasksDic = getListOfTask(selectedCat, uid)
        if someThingsChanged:
                UserResult.objects.update_or_create(
                        user=uid,
                        defaults={"Change": True}
                )
        return render(request, "assessment/taskPage.html", {"categoriesPI":categories,
                                                            "catIdPI":catId,
                                                            "PIPhoto":'/'.join(selectedCat.photo.url.split('/')[3:]),
                                                            "catName":selectedCat.category,
                                                            "tasksList": tasksDic
                                                            }) 


@login_required(login_url= '/auth/login')
def profilePage(request):
        uid = User.objects.get(id=request.user.id)
        username=""
        email=""
        companyname=""
        country=""
        industry=""
        profile  = myprofile.objects.get(user=uid)
        if(profile):
                username = uid.username
                email = uid.email
                country = profile.country.country
                industry = profile.industry.industry
                companyname = profile.company_name
        return render(request, "assessment/profilePage.html", {
                "username":username,
                "email":email,
                "companyname":companyname,
                "country":country,
                "industry":industry,

        })
        
