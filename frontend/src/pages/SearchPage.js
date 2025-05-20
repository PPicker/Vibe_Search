import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './SearchPage.css';





const SearchPage = () => {
    const [query, setQuery] = useState('');
    const [results, setResults] = useState([]);
    const [isLoading, setIsLoading] = useState(false);
    const navigate = useNavigate();

    const handleSearch = async () => {
        if (!query.trim()) {
            alert('검색어를 입력해주세요');
            return;
        }


        setIsLoading(true);
        try {
            const response = await fetch('/api/search', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ query }),
            });

            if (!response.ok) {
                throw new Error('검색 중 오류가 발생했습니다');
            }

            const data = await response.json();
            setResults(data);
        } catch (error) {
            console.error('검색 오류:', error);
            alert('검색 중 오류가 발생했습니다');
        } finally {
            setIsLoading(false);
        }
    };

    const goToProductDetail = (productId) => {
        navigate(`/product/${productId}`);
    };

    return (
        <div className="search-page">
            <div className="search-header">
                <h1>VIBE SEARCH</h1>
                <p className="subtitle">당신이 찾는 스타일을 자유롭게 설명해주세요</p>
            </div>

            <div className="search-example">
                <p className="example-text">
                    예시: "도쿄의 빈티지 숍에서 찾을 것 같은 워크웨어 자켓" 또는 "미니멀한 디자인의 오버사이즈 니트"
                </p>
            </div>

            <div className="search-box">
                <input
                    type="text"
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="원하는 스타일을 설명해보세요"
                    className="search-input"
                    onKeyPress={(e) => e.key === 'Enter' && handleSearch()}
                />
                <button onClick={handleSearch} className="search-button">
                    SEARCH
                </button>
            </div>

            <div className="search-categories">
                <h2>이런 것들을 설명해보세요</h2>
                <div className="categories-grid">
                    <div className="category-card">
                        <h3>스타일 & 분위기</h3>
                        <p>"미니멀한", "빈티지한", "스트릿", "클래식" 등</p>
                    </div>
                    <div className="category-card">
                        <h3>디테일 & 특징</h3>
                        <p>"오버사이즈 핏", "워시드 데님", "짧은 디테일" 등</p>
                    </div>
                    <div className="category-card">
                        <h3>상황 & 용도</h3>
                        <p>"데일리룩", "캠퍼스", "데이트" 등 어떤 상황이</p>
                    </div>
                    <div className="category-card">
                        <h3>감색 예시</h3>
                        <p>"요즘 인스타에서 유행하는 테크웨어", "일본 0</p>
                    </div>
                </div>
            </div>

            {isLoading ? (
                <div className="loading">검색 중...</div>
            ) : (
                results.length > 0 && (
                    <div className="search-results">
                        {results.map((product) => (
                            <div className="product-card" key={product.id}>
                                <div className="product-image">
                                    {product.image_url && (
                                        <img src={product.image_url} alt={product.name} />
                                    )}
                                </div>
                                <div className="product-info">
                                    <h3>{product.name}</h3>
                                    <p className="price">₩ {product.price.toLocaleString()}</p>
                                    {/* 간단한 설명 표시 (옵션) */}
                                    {product.description && (
                                        <p className="product-brief-desc">
                                            {tryParseDescription(product.description)}
                                        </p>
                                    )}
                                    <div className="product-actions">
                                        <a href={product.link} target="_blank" rel="noopener noreferrer" className="buy-link">
                                            구매 링크 ▶
                                        </a>
                                        <button
                                            className="detail-button"
                                            onClick={() => goToProductDetail(product.id)}
                                        >
                                            자세히 보기 ▶
                                        </button>
                                    </div>
                                </div>
                            </div>
                        ))}
                    </div>
                )
            )}
        </div>
    );
};

// 설명 데이터 간단히 파싱하는 함수
function tryParseDescription(description) {
    if (!description) return '';

    try {
        // JSON 형식인지 확인
        if (typeof description === 'string' &&
            (description.startsWith('{') || description.startsWith('['))) {
            const descObj = JSON.parse(description);

            // 객체인 경우 첫 번째 키-값 쌍만 반환
            if (descObj && typeof descObj === 'object' && !Array.isArray(descObj)) {
                const keys = Object.keys(descObj);
                if (keys.length > 0) {
                    return `${keys[0]}: ${descObj[keys[0]]}`;
                }
            }
        }

        // 그 외의 경우 문자열 그대로 반환 (50자로 제한)
        return description.length > 50
            ? description.substring(0, 50) + '...'
            : description;
    } catch (e) {
        console.error('Error parsing description:', e);
        return description.length > 50
            ? description.substring(0, 50) + '...'
            : description;
    }
}

export default SearchPage;