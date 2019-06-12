from selenium import webdriver

def parsePolygonPoints(s):
    '''
    parse coordinates string retrieved 
    into float lists of x-coordinates and y-coordinates
    '''
    x = []
    y = []
    for coords_str in s.split():
        coords = coords_str.split(',')
        x.append(float(coords[0]))
        y.append(float(coords[1]))
    return (x, y)

def shoelace(x, y):
    '''
    Shoelace algorithm:
    '''
    res = 0
    for i in range(len(x)-1):
        res += x[i]*y[i+1] - x[i+1]*y[i]
    res += x[-1]*y[0] - x[0]*y[-1]
    return abs(res)/2

def pipeline(polygons):
    '''
    take selenium web element of polygon tag
    and return the index of bigger shape
    '''
    coords_str_shape0 = polygons[0].get_attribute('points')
    coords_str_shape1 = polygons[1].get_attribute('points')

    # bigger_one = False == 0 when shape0 larger than shape1
    bigger_one = int(shoelace(*parsePolygonPoints(coords_str_shape0))
                     < shoelace(*parsePolygonPoints(coords_str_shape1)))

    return bigger_one

if __name__ == '__main__':

    # initialize webdriver
    driver = webdriver.Safari()

    # open browser
    url = 'https://pick-the-bigger-shape.herokuapp.com'
    driver.get(url)

    # click the start button
    btn = driver.find_element_by_id('start-button')
    btn.click()

    while True:
        polygons = driver.find_elements_by_tag_name('polygon')
        bigger_one = pipeline(polygons)
        driver.find_element_by_id('shape' + str(bigger_one)).click()
