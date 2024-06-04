import { useEffect, useState } from "react";
import banner from "../banner.jpg";
import { Link } from "react-router-dom";
import Filter from "./Filter";
import FlatList from "./FlatList";

const Banner = () => {
    const [search, setSearch] = useState([]);
    const [find, setFind] = useState([]);
    const [word, setWord] = useState("");
    const [showFilter, setShowFilter] = useState(false); // State for managing the Filter visibility
    const [icon, setIcon] = useState("fa-filter"); // State for managing the icon

    // Filter state
    const [filters, setFilters] = useState({
      posredovanje: "",
      tip_nepremicnine: "",
      lokacija: "",
      cenaMin: null,
      cenaMax: null,
      st_sob: null,
      st_spalnic: null,
      st_kopalnic: null,
      leto_izgradnje: null,
      st_nadstropij: null,
      velikost_zemljiscaMin: null,
      velikost_zemljiscaMax: null,
      velikost_skupajMin: null,
      velikost_skupajMax: null,
      agencija: ""
    });

    useEffect(() => {
        setSearch(["a", "b", "test", "mb"]);
    }, []);

    const findSearch = (e) => {
        setWord(e.target.value);
        const filteredCountries = search.filter(item => item.indexOf(e.target.value) > -1 ? item : null);
        e.target.value.length === 0 ? setFind([]) : setFind(filteredCountries);
    };

    const findResult = () => {
        if (find.length === 0 && word.length > 0) {
            return <div className="find-search">Not Found</div>;
        }
        if (find.length > 0) {
            return (
                <div className="find-search">
                    {find.map(item => {
                        return <Link key={item} to="#">{item}</Link>;
                    })}
                </div>
            );
        }
    };

    const handleFilterButtonClick = () => {
        setShowFilter(!showFilter);
        setIcon(showFilter ? "fa-filter" : "fa-times");
    };

    const handleCloseFilter = () => {
        setShowFilter(false);
        setIcon("fa-filter");
    };

    const handleApplyFilters = (newFilters) => {
        setFilters(newFilters);
        setShowFilter(false);
        setIcon("fa-filter");
    };

    return (
      <div>
        <div className="banner d-flex align-items-center" style={{ backgroundImage: `url(${banner})` }}>
            <div className="bg-custom">
                <div className="container">
                    <div className="row">
                        <div className="col-lg-6 mx-auto">
                            <div className="banner-area text-center pt-4 pb-4">
                                <p>Text</p>
                                <h2 className="mt-2 mb-4 banner-title"><strong>NASLOV</strong></h2>
                                <div className="search-area">
                                    <button
                                        className="btn-filter m-2"
                                        title='Filtriraj'
                                        onClick={handleFilterButtonClick}
                                        style={{outline: 'none'}}
                                    >
                                        <i className={`fa ${icon}`} aria-hidden="true"></i>
                                    </button>
                                    <input
                                        value={word}
                                        onChange={(e) => findSearch(e)}
                                        type="text"
                                        className="inp-search"
                                        placeholder="Išči..."
                                    />
                                    <button className="btn-search m-2">Išči</button>
                                </div>
                                {findResult()}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {showFilter && <Filter filters={filters} onClose={handleCloseFilter} onApply={handleApplyFilters} />}
        <FlatList filters={filters} />
      </div>
    );
};

export default Banner;