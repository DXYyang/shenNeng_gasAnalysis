import base64
from .. import db
import os
import  math
from . import main
from ..models import Role,ImageFile,User,Portrait,ConsumptionUseCase
import imghdr
from .forms import upForm,EditProfileForm,SearchForm,EditProfileAdminForm,KMeansForm,LogicPredictionForm,Intel_consumptionForm,Review_sentimentForm,GasProblemDistributionForm
from flask_login import login_required,current_user
from flask import render_template,session,redirect,url_for,abort,flash,request,current_app,make_response,json,jsonify
from sqlalchemy import or_,create_engine
from ..decorators import admin_required,gas_analysis_required,customer_required
from .analysis.K_means import density_plot
from .analysis.gas_sentence_cut import read_file_cut
from.analysis.gas_problem_distribute import gas_problem_distribute
from .analysis.Logic_Regression import Logic_Regression_plot,train_data
from .analysis.gas_kmeans_plt import gas_kmeans_pit
from random import randint
from .sentiment_analysis.dictionary_feature import single_review_sentiment_score
@main.route('/',methods=['GET','POST'])
def index():
    portrait=None
    if current_user.is_authenticated:
        user = User.query.filter_by(username=current_user.username).first()
        if user is None:
            abort(404)
        portrait = Portrait.query.filter_by(user=user).first()
    return render_template('index.html',portrait=portrait,base64=base64)
@main.route('/upload',methods=['GET','POST'])
@login_required
def upload():
    user = User.query.filter_by(username=current_user.username).first()
    if user is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=user).first()
    ds=ImageFile.query.filter_by(user=current_user).all()
    form=upForm()
    if request.method == 'POST' and form.validate_on_submit():
        if imghdr.what(request.files['file']) is not None:
            file = request.files['file'].read()
            file_name = form.name.data
            image_file = ImageFile(image_name=file_name, image=file,user=current_user)
            db.session.add(image_file)
            db.session.commit()
            flash('ok')
        else:
            flash('This is not a picture!')
        return redirect(url_for('.upload'))
    return render_template('upload.html', form=form, ds=ds, base64=base64,portrait=portrait)
@main.route('/edit_profile',methods=['GET','POST'])
@login_required
def edit_profile():
    form=EditProfileForm()
    user = User.query.filter_by(username=current_user.username).first()
    if user is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=user).first()
    if form.validate_on_submit():
        current_user.name=form.name.data
        current_user.location=form.location.data
        current_user.about_me=form.about_me.data
        db.session.add(current_user)
        flash('你的个人信息已更新！')
        return redirect(url_for('.user_info',username=current_user.username))
    form.name.data=current_user.name
    form.location.data=current_user.location
    form.about_me.data=current_user.about_me
    return render_template('edit_profile.html',form=form,portrait=portrait,base64=base64)
@main.route('/user_info/<username>')
def user_info(username):
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    user=User.query.filter_by(username=username).first()
    if user is None:
        abort(404)
    portrait_user=Portrait.query.filter_by(user=user).first()
    return render_template('user_info.html',user=user,portrait=portrait,portrait_user=portrait_user,base64=base64)
@main.route('/admin_userlist',methods=['GET','POST'])
@login_required
@admin_required
def admin_userlist():
    user = User.query.filter_by(username=current_user.username).first()
    if user is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=user).first()
    users=User.query.all()
    form=SearchForm()
    if form.validate_on_submit():
        searchinfo=form.search.data
        rule='%'+searchinfo+'%'
        users=User.query.filter(or_(User.name.like(rule),User.username.like(rule))).all()
        return render_template('admin_userlist.html', form=form, users=users,portrait=portrait,base64=base64)
    return render_template('admin_userlist.html',form=form,users=users,portrait=portrait,base64=base64)
@main.route('/admin_edit_userinfo/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def admin_edit_userinfo(id):
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    user=User.query.get_or_404(id)
    form=EditProfileAdminForm(user=user)
    if form.validate_on_submit():
        user.email=form.email.data
        user.username=form.username.data
        user.role=Role.query.get(form.role.data)
        user.name=form.name.data
        user.location=form.location.data
        user.about_me=form.about_me.data
        db.session.add(user)
        flash('用户信息已被更新.')
        return redirect(url_for('.user_info',username=user.username))
    form.email.data=user.email
    form.username.data=user.username
    form.role.data=user.role_id
    form.name.data=user.name
    form.location.data=user.location
    form.about_me.data=user.about_me
    return render_template('admin_edit_userinfo.html',form=form,user=user,portrait=portrait,
                           base64=base64)
@main.route('/K_means',methods=['GET','POST'])
@login_required
@gas_analysis_required
def K_means():
    form=KMeansForm()
    k=0
    picture_url = []
    series=[]
    values=[]
    labels=[]
    import pandas as pd
    variety_means=pd.DataFrame
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    if form.validate_on_submit():
        k=int(form.KMeans.data)
        import pandas as pd
        outputfile = 'app/main/analysis/tmp/data_type.xls'  # 保存结果的文件名
        outputfile1 = 'app/main/analysis/tmp/data_type1.xls'  # 保存结果的文件名
        engine=create_engine('mysql+pymysql://root:diaoxuyang@localhost:3306/gas_info')
        iteration = 500  # 聚类最大循环次数
        data = pd.read_sql('customers',engine,index_col='id') # 读取数据
        data_zs = 1.0 * (data - data.mean()) / data.std()  # 数据标准化
        from sklearn.cluster import KMeans
        model = KMeans(n_clusters=k, n_jobs=1, max_iter=iteration)  # 分为k类，并发数
        model.fit(data_zs)  # 开始聚类
        r1 = pd.Series(model.labels_).value_counts()  # 统计各个类别的数目
        r2 = pd.DataFrame(model.cluster_centers_)  # 找出聚类中心
        r = pd.concat([r2, r1], axis=1)  # 横向连接（0是纵向），得到聚类中心对应的类别下的数目
        r.columns = list(data.columns) + [u'类别数目']  # 重命名表头
        r.to_excel(outputfile1)  # 保存结果
        frame = pd.read_excel(outputfile1)
        category = frame['类别数目']
        cate_length = len(category)
        for value in category:
            values.append(value)
        for i in range(cate_length):
            labels.append(u'第' + str(i + 1) + '类客户')
        r = pd.concat([data, pd.Series(model.labels_, index=data.index)], axis=1)  # 详细输出每个样本对应的类别
        r.columns = list(data.columns) + [u'聚类类别']  # 重命名表头
        variety_means=r[['year_avg_use','high_usage_rate','capacity','replace_thing','grow_rate']].groupby(r['聚类类别']).mean().round(3)
        r.to_excel(outputfile)  # 保存结果
        pic_output = 'app/static/pd_'  # 概率密度图文件名前缀
        customer_map={}
        data_list=[]
        for i in range(k):
            density_plot(data[r[u'聚类类别'] == i],5).savefig(u'%s%s.png' % (pic_output, i))
            picture='pd_'+str(i)+'.png'
            picture_url.append(picture)
            data_list.append(variety_means['high_usage_rate'][i])
            data_list.append(variety_means['capacity'][i])
            data_list.append(variety_means['grow_rate'][i])
            customer_map['data']=data_list
            data_list=[]
            customer_map['name'] = '客户' + str(i + 1)
            series.append(customer_map)
            customer_map = {}
    return render_template('K_means.html',form=form,k=range(k),picture_url=picture_url,randint=randint,variety_means=variety_means,
                           series=series,portrait=portrait,base64=base64,values=values,labels=labels)
ALLOWED_EXTENSIONS = set(['csv', 'xls'])
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
@main.route('/Logic_regression')
@login_required
@gas_analysis_required
def Logic_regression():
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    import pandas as pd
    result=pd.DataFrame()
    coef = pd.DataFrame()
    Logic_pic = None
    predict_form = LogicPredictionForm()
    return render_template('Logic_regression.html', predict_form=predict_form, Logic_pic=Logic_pic,
                           randint=randint, result=result, coef=coef,portrait=portrait,base64=base64)
@main.route('/Logic_property',methods=['POST'])
@login_required
@gas_analysis_required
def Logic_property():
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    import pandas as pd
    result_from_db=None
    coef = pd.DataFrame()
    predict_form = LogicPredictionForm()
    from sqlalchemy import create_engine
    import pandas as pd
    engine = create_engine('mysql+pymysql://root:diaoxuyang@localhost:3306/gas_info')
    origin_data = pd.read_sql('gasconsumption', engine)
    Logic_output = 'app/static/Logic_pic'
    Logic_pic = 'Logic_pic.png'
    Logic_Regression_plot(origin_data).savefig(u'%s.png' % (Logic_output))
    return render_template('Logic_regression.html', predict_form=predict_form, Logic_pic=Logic_pic,
                           randint=randint, result_from_db=result_from_db, coef=coef,portrait=portrait,base64=base64)
@main.route('/Logic_prediction',methods=['GET','POST'])
@login_required
@gas_analysis_required
def Logic_prediction():
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    from ..models import GasPredictionSale
    page = request.args.get('page', 1, type=int)
    pagination = GasPredictionSale.query.order_by(GasPredictionSale.id).paginate(
        page, per_page=current_app.config['FLASKY_LOGIC_PER_PAGE'],
        error_out=False)
    result_from_db = pagination.items
    import pandas as pd
    coef =pd.DataFrame()
    Logic_pic = None
    predict_form = LogicPredictionForm()
    if predict_form.validate_on_submit():
        file = request.files['file']
        if file and allowed_file(file.filename):
            file_url = os.path.join(os.getcwd(), file.filename)
            from sqlalchemy import create_engine
            from ..models import GasPredictionSale
            import pandas as pd
            engine = create_engine('mysql+pymysql://root:diaoxuyang@localhost:3306/gas_info')
            origin_data = pd.read_sql('gasconsumption', engine)
            import pandas as pd
            import numpy as np
            predict_data= pd.read_excel(file_url).filter(regex='gas_sales|district_.*|population|month_.*|gas_price|liquid_price')
            predictions=train_data(origin_data).predict(predict_data)
            origin_data=origin_data.filter(regex='gas_sales|sales_well|district_.*|population|month_.*|gas_price|liquid_price')
            result = pd.DataFrame({'gas_sales': predict_data['gas_sales'].astype(np.int32).as_matrix(), 'sales_well': predictions.astype(np.int32)})
            for index,row in result.iterrows():
                GasPredictionSale1=GasPredictionSale(gas_sales=int(row['gas_sales']),sales_well=int(row['sales_well']))
                db.session.add(GasPredictionSale1)
            db.session.commit()
            pagination = GasPredictionSale.query.order_by(GasPredictionSale.id).paginate(
                page, per_page=current_app.config['FLASKY_LOGIC_PER_PAGE'],
                error_out=False)
            result_from_db =pagination.items
            coef = pd.DataFrame({"columns": list(origin_data.columns)[1:], "coef": list(train_data(origin_data).coef_.T)})
        else:
            from sqlalchemy import create_engine
            from ..models import GasPredictionSale
            import pandas as pd
            import numpy as np
            engine = create_engine('mysql+pymysql://root:diaoxuyang@localhost:3306/gas_info')
            origin_data = pd.read_sql('gasconsumption', engine)
            predict_data = pd.read_sql('gasconsumptiontest', engine).filter(regex='gas_sales|district_.*|population|month_.*|gas_price|liquid_price')
            predictions=train_data(origin_data).predict(predict_data)
            origin_data = origin_data.filter(regex='gas_sales|sales_well|district_.*|population|month_.*|gas_price|liquid_price')
            result = pd.DataFrame({'gas_sales': predict_data['gas_sales'].astype(np.int32).as_matrix(), 'sales_well': predictions.astype(np.int32)})
            for index,row in result.iterrows():
                GasPredictionSale1=GasPredictionSale(gas_sales=int(row['gas_sales']),sales_well=int(row['sales_well']))
                db.session.add(GasPredictionSale1)
            db.session.commit()
            pagination = GasPredictionSale.query.order_by(GasPredictionSale.id).paginate(
                page, per_page=current_app.config['FLASKY_LOGIC_PER_PAGE'],
                error_out=False)
            result_from_db = pagination.items
            coef = pd.DataFrame({"columns": list((origin_data.columns)[1:]), "coef": list(train_data(origin_data).coef_.T)})
    return render_template('Logic_prediction.html',predict_form=predict_form,
                           Logic_pic=Logic_pic,randint=randint, result_from_db=result_from_db,
                           coef=coef,pd=pd,pagination=pagination,portrait=portrait,base64=base64)
@main.route('/delPic/<int:id>',methods=['GET'])
@login_required
def delPic(id):
    db.session.query(ImageFile).filter_by(id=id).delete()
    db.session.commit()
    flash('ok')
    return redirect(url_for('.upload'))
@main.route('/changePic/<int:id>/<username>', methods=['GET'])
@login_required
def changePic(id,username):
    newimage= ImageFile.query.filter_by(id=id).first()
    user = User.query.filter_by(username=username).first()
    result = Portrait.query.filter_by(user=user).first()
    if result is not None:
        db.session.delete(result)
    portrait = Portrait(imagefile=newimage, user=user, image_name=newimage.image_name,image=newimage.image)
    db.session.add(portrait)
    db.session.commit()
    flash('ok')
    return redirect(url_for('main.user_info',username=user.username))
@main.route('/Intel_consumption',methods=['POST','GET'])
@login_required
@customer_required
def Intel_consumption():
    form=Intel_consumptionForm()
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    if form.validate_on_submit():
        family_numbers=int(form.family_numbers.data)
        month_avg_income=int(form.avg_month_income.data)
        province=request.form['province']
        city=request.form['city']
        town=request.form['town']
        place=province+city+town
        max_fn=ConsumptionUseCase.query.filter_by(place=place).order_by(db.desc(ConsumptionUseCase.family_numbers)).first()
        if(max_fn is None):
            flash('Not find the UserCase!')
            return render_template('Intel_consumption.html',form=form)
        model_customers = ConsumptionUseCase.query.filter_by(place=place).all()
        min_fn=ConsumptionUseCase.query.filter_by(place=place).order_by(ConsumptionUseCase.family_numbers).first()
        range_fn=max_fn.family_numbers-min_fn.family_numbers
        max_in = ConsumptionUseCase.query.filter_by(place=place).order_by(
            db.desc(ConsumptionUseCase.month_avg_income)).first()
        min_in = ConsumptionUseCase.query.filter_by(place=place).order_by(
            ConsumptionUseCase.month_avg_income).first()
        range_in=max_in.month_avg_income-min_in.month_avg_income
        UserCases=ConsumptionUseCase.query.filter_by(place=place).all()
        mindistance=999
        similar_case=None
        for Usercase in UserCases:
            mresult1=(abs(Usercase.family_numbers-family_numbers)/range_fn)**2
            mresult2=(abs(Usercase.month_avg_income-month_avg_income)/range_in)**2
            if math.sqrt(mresult1+mresult2)<mindistance:
                mindistance=math.sqrt(mresult1+mresult2)
                similar_case=Usercase
        return render_template('Intel_recommend.html',place=place,similar_case=similar_case,
                               model_customers=model_customers,family_numbers=family_numbers,
                               month_avg_income=month_avg_income,portrait=portrait,base64=base64)
    return  render_template('Intel_consumption.html',form=form,base64=base64,portrait=portrait)
@main.route('/Review_senti', methods=['GET', 'POST'])
@login_required
@gas_analysis_required
def Review_senti():
    result =[]
    form=Review_sentimentForm()
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    review_title=['积极得分','消极得分','积极均值','消极均值','积极标准差','消极标准差']
    if form.validate_on_submit():
        result = single_review_sentiment_score(form.Review.data)
        percentage=[result[0],result[1]]
        return render_template('Review_senti.html', result=result,form=form,review_title=review_title,
                               k=range(6),percentage=percentage,portrait=portrait,base64=base64)
    return render_template('Review_senti.html', result=result,form=form,review_title=review_title,
                           k=range(6),portrait=portrait,base64=base64)

@main.route('/Gasproblem_distribute',methods=['GET','POST'])
@login_required
@gas_analysis_required
def Gasproblem_distribute():
    form=GasProblemDistributionForm()
    k = 0
    topsix_keyword=[]
    words_rank=[]
    pie_list=[]
    picture_url=None
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    if form.validate_on_submit():
        k=int(form.KMeans.data)
        read_file_cut()
        weight=gas_problem_distribute(k)['weight']
        clf=gas_problem_distribute(k)['clf']
        word=gas_problem_distribute(k)['word']
        dist=gas_problem_distribute(k)['dist']
        s = clf.fit(weight)
        clusters = clf.labels_.tolist()
        import pandas as pd
        catagory_counts = pd.Series(clf.labels_).value_counts()
        cata_index=list(catagory_counts.index)
        for index,data in enumerate(catagory_counts):
            pie_name='第'+str(cata_index[index]+1)+'类问题'
            pie_list.append([pie_name,data])
        order_centroids = clf.cluster_centers_.argsort()[:, ::-1]# 按离聚类中心的距离排列类集，由近到远
        for i in range(k):
            for ind in order_centroids[i, :6]:#选取最近的6个词的编号
                topsix_keyword.append(word[ind])
            words_rank.append(topsix_keyword)
            topsix_keyword=[]
        pie_output = 'app/static/gas_kmeans'
        gas_kmeans_pit(dist, words_rank, clusters).savefig(u'%s.png' % (pie_output))
        picture_url='gas_kmeans.png'
        return render_template('Gasproblem_distribute.html', form=form, words_rank=words_rank, enumerate=enumerate,
                               pie_list=pie_list, picture_url=picture_url,portrait=portrait,base64=base64,k=k)
    return render_template('Gasproblem_distribute.html',form=form,words_rank=words_rank,enumerate=enumerate,
                           pie_list=pie_list,picture_url=picture_url,portrait=portrait,base64=base64,k=k)
@main.route('/Customer_list',methods=['GET','POST'])
@login_required
@gas_analysis_required
def Customer_list():
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    from ..models import Customer
    page = request.args.get('page', 1, type=int)#默认取第一页
    pagination =Customer.query.order_by(Customer.id).paginate(
        page, per_page=current_app.config['FLASKY_LOGIC_PER_PAGE'],
        error_out=False)
    return render_template('Customer_list.html',pagination=pagination,
                           result_from_db = pagination.items,portrait=portrait,base64=base64)
@main.route('/gas_fix',methods=['GET','POST'])
@login_required
@customer_required
def gas_fix():
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    return render_template('gas_fix.html',portrait=portrait,base64=base64)
@main.route('/history_based_recommend',methods=['GET','POST'])
@login_required
@gas_analysis_required
def history_based_recommend():
    loginUser = User.query.filter_by(username=current_user.username).first()
    if loginUser is None:
        abort(404)
    portrait = Portrait.query.filter_by(user=loginUser).first()
    import pandas as pd
    from math import ceil
    data = pd.read_excel('app/main/analysis/data/timeuse.xls', index_col=0)#month为索引
    last_year_data=list(data['2016-1-01':]['use'])
    from statsmodels.tsa.arima_model import ARMA
    dta = data.diff(1)[1:]#差分处理，提高序列稳定性
    arma_mod01 = ARMA(dta, (10, 1)).fit()
    predict_sunspots = arma_mod01.predict('2017-1-01', '2017-12-01', dynamic=True)
    predict_sunspots[0] =ceil(predict_sunspots[0]+data['2016-12-01':]['use'])
    for i in range(len(predict_sunspots) - 1):
        predict_sunspots[i + 1] =ceil(predict_sunspots[i] + predict_sunspots[i + 1])
    data=list(predict_sunspots)
    return render_template('history_based_recommend.html',data=data,last_year_data=last_year_data,portrait=portrait,base64=base64)

