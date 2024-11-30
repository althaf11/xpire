from flask import Flask, render_template, request, url_for, flash, redirect
from datetime import date, timedelta, datetime
from operator import itemgetter

# Create a flask app
app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static'
)

app.config['SECRET_KEY'] = 'b9fb4a2e41544f4dfe25a9c1' 


items = []
empty = []
daysPrior = 2

# Index page (now using the index.html file)
@app.route('/')
def index():
  return render_template('index.html', items=items)

 


@app.route('/create', methods=('GET', 'POST'))
def create():
  if request.method == 'POST':
    grocery = request.form['grocery']
    expiry = request.form['expiry']

    if not grocery:
      flash('Please input your grocery item!')
    elif not expiry:
      flash('Please input the expiry date!')
    else:
      items.append({'grocery': grocery, 'expiry': expiry}) 
      return redirect(url_for('index'))
  return render_template('create.html')  

@app.route('/index', methods=["DELETE"]) 
def remove():
  if request.method == 'DELETE':
    grocery = request.form['grocery']
    expiry = request.form['expiry']
    items.remove({'grocery': grocery, 'expiry': expiry}) 
    return redirect(url_for('index'))
  return render_template('create.html') 
  
def expirybutton():
    today = date.today()
    days = timedelta(daysPrior)
    new_date = today + days
    product = ()
    productList = []
    for item in items:
      for i in item:
          if i == 'grocery':
              product = item[i]
          if i == 'expiry':
              if (datetime.strptime(item[i], '%Y-%m-%d').date()) <= new_date:
                productList.append(product)
    if not productList:
    #empty list is false
      return "You have no items that are within " + str(daysPrior) + " days of their expiry date."

    else:
      newProductList=(', '.join(productList))
      return "Your grocery items that are expiring within " + str(daysPrior) + " days: " + newProductList 
expirybutton()

@app.route('/expiry')
def expiryPage():
    return render_template('expiry.html', myfunction=expirybutton)

@app.route('/remove')
def removePage():
    product = ()
    listOfProds = []
    for item in items:
      for i in item:
          if i == 'grocery':
              product = item[i]
              listOfProds.append(product)
    return render_template('remove.html', myproducts=listOfProds)


@app.route('/remove', methods=['POST'])
def removeItem():
  if request.method == 'POST':
    selection = request.form.get('dropSelection')
    for item in items: 
      if item['grocery'] == selection:
        index = items.index(item) 
        items.pop(index)
  return redirect(url_for('index'))

  
if __name__ == '__main__':
  # Run the Flask app
  app.run(
	host='0.0.0.0',
	debug=True,
	port=8080
  )
