import { useEffect, useState } from "react"
import banner from "../banner.jpg"
import { Link } from "react-router-dom";

const Banner = () => {
    const [search, setSearch] = useState();
    const [find, setFind] = useState([]);
    const [word, setWord] = useState("");
    useEffect(() => {
        setSearch(["a","b","test", "mb"])
    }, [])

    const findSearch = (e) => {
        setWord(e.target.value)
        const filteredCountries = search.filter(item => item.indexOf(e.target.value) > -1 ? item : null);
        e.target.value.length === 0 ? setFind([]) : setFind(filteredCountries);
    }

    const findResult = () => {
        if (find.length === 0 && word.length > 0) {
            return <div className="find-search">Not Found</div>
        }
        if (find.length > 0) {
            return <div className="find-search">
                {
                    find.map(item => {
                        return <Link key={item} to="#">{item}</Link>
                    })
                }
            </div>
        }
    }

    return (
      <div className="banner d-flex align-items-center" style={{ backgroundImage: `url(${banner})` }}>
      <div className="bg-custom">
          <div className="container">
              <div className="row">
                  <div className="col-lg-6 mx-auto">
                      <div className="banner-area text-center pt-4 pb-4">
                          <p>Text</p>
                          <h2 className="mt-2 mb-4 banner-title"><strong> NASLOV</strong> </h2>
                          <div className="search-area">
                              <Link  className="btn-filter m-2" to="/filtri" title='Filtriraj'><i class="fa fa-filter" aria-hidden="true"></i></Link>
                              <input value={word} onChange={(e) => findSearch(e)} type="text" className="inp-search" placeholder="Išči..." />
                              <button className="btn-search m-2">Išči</button>
                          </div>
                          {findResult()}
                      </div>
                  </div>
              </div>
          </div>
      </div>
  </div>
    )
}

export default Banner;