// import { useEffect, useState } from 'react';
// import { useNavigate, useParams } from 'react-router-dom';
// import './ProductDetailPage.css';

// const ProductDetailPage = () => {
//     const { id } = useParams();
//     const [product, setProduct] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);
//     const [selectedImage, setSelectedImage] = useState(0);
//     const navigate = useNavigate();

//     useEffect(() => {
//         const fetchProductDetail = async () => {
//             try {
//                 const response = await fetch(`/api/product/${id}`);

//                 if (!response.ok) {
//                     throw new Error('상품을 찾을 수 없습니다.');
//                 }

//                 const data = await response.json();
//                 setProduct(data);
//             } catch (err) {
//                 console.error('Error fetching product:', err);
//                 setError(err.message);
//             } finally {
//                 setLoading(false);
//             }
//         };

//         fetchProductDetail();
//     }, [id]);

//     const handleGoBack = () => {
//         navigate(-1);
//     };

//     // 설명 데이터 파싱하는 함수
//     const parseProductDetails = (description) => {
//         if (!description) return [];

//         if (typeof description === 'object') {
//             return Object.entries(description)
//                 .filter(([key, value]) => value !== null && value !== "")
//                 .map(([key, value]) => ({
//                     label: key,
//                     value: typeof value === 'string' ? value : JSON.stringify(value)
//                 }));
//         }


//         try {
//             // JSON 형식인 경우
//             if (typeof description === 'string' &&
//                 (description.startsWith('{') || description.startsWith('['))) {
//                 const descObj = JSON.parse(description);

//                 // 객체인 경우
//                 if (descObj && typeof descObj === 'object' && !Array.isArray(descObj)) {
//                     return Object.entries(descObj)
//                         .filter(([key, value]) => value !== null && value !== '')
//                         .map(([key, value]) => ({
//                             label: key,
//                             value: typeof value === 'string' ? value : JSON.stringify(value)
//                         }));
//                 }
//             }

//             // 일반 문자열인 경우 - 줄바꿈으로 분리
//             return description.split('\n')
//                 .filter(line => line.trim())
//                 .map(line => {
//                     const parts = line.split(':');
//                     if (parts.length > 1) {
//                         return {
//                             label: parts[0].trim(),
//                             value: parts.slice(1).join(':').trim()
//                         };
//                     }
//                     return { label: '', value: line.trim() };
//                 });
//         } catch (e) {
//             console.error('Error parsing description:', e);
//             return [{ label: '', value: description }];
//         }
//     };

//     if (loading) {
//         return <div className="loading">로딩 중...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <p className="error-message">{error}</p>
//                 <button className="back-button" onClick={handleGoBack}>
//                     ⬅ 뒤로 가기
//                 </button>
//             </div>
//         );
//     }

//     // 상품 설명 파싱
//     const details = product?.description
//         ? parseProductDetails(product.description)
//         : [];

//     return (
//         <div className="product-detail-page">
//             <div className="product-container">
//                 <div className="product-gallery">
//                     <div className="main-image">
//                         {product?.image_urls && product.image_urls.length > 0 ? (
//                             <img
//                                 src={product.image_urls[selectedImage]}
//                                 alt={product.name}
//                                 className="featured-image"
//                             />
//                         ) : (
//                             <div className="no-image">이미지가 없습니다</div>
//                         )}
//                     </div>

//                     <div className="thumbnail-gallery">
//                         {product?.image_urls?.map((url, index) => (
//                             <div
//                                 key={index}
//                                 className={`thumbnail ${selectedImage === index ? 'selected' : ''}`}
//                                 onClick={() => setSelectedImage(index)}
//                             >
//                                 <img src={url} alt={`${product.name} - 이미지 ${index + 1}`} />
//                             </div>
//                         ))}
//                     </div>
//                 </div>

//                 <div className="product-info">
//                     <h1 className="product-name">{product?.name}</h1>
//                     <p className="product-price">₩ {product?.price?.toLocaleString()}</p>

//                     <div className="product-actions">
//                         <a
//                             href={product?.link}
//                             target="_blank"
//                             rel="noopener noreferrer"
//                             className="buy-now-button"
//                         >
//                             BUY NOW
//                         </a>
//                         <button className="add-to-cart-button">ADD TO CART</button>
//                     </div>

//                     <div className="product-details">
//                         <h2>PRODUCT DETAILS</h2>
//                         <ul>
//                             {details.length > 0 ? (
//                                 details.map((item, index) => (
//                                     <li key={index}>
//                                         {item.label && <strong>{item.label}</strong>}
//                                         {item.label && ': '}
//                                         {item.value}
//                                     </li>
//                                 ))
//                             ) : (
//                                 // 기본 정보 표시 (설명 데이터가 없을 경우)
//                                 <>
//                                     <li>Material: 100% Cotton</li>
//                                     <li>Made in Korea</li>
//                                     <li>Care Instructions: Machine wash cold</li>
//                                     <li>Regular fit</li>
//                                     <li>Model is wearing size M</li>
//                                 </>
//                             )}
//                         </ul>
//                     </div>

//                     <button className="back-button" onClick={handleGoBack}>
//                         ⬅ 검색 결과로 돌아가기
//                     </button>
//                 </div>
//             </div>
//         </div>
//     );
// };

// export default ProductDetailPage;

// import { useEffect, useState } from 'react';
// import { useNavigate, useParams } from 'react-router-dom';
// import './ProductDetailPage.css';

// const ProductDetailPage = () => {
//     const { id } = useParams();
//     const [product, setProduct] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);
//     const [selectedImage, setSelectedImage] = useState(0);
//     const navigate = useNavigate();

//     useEffect(() => {
//         const fetchProductDetail = async () => {
//             try {
//                 const response = await fetch(`/api/product/${id}`);

//                 if (!response.ok) {
//                     throw new Error('상품을 찾을 수 없습니다.');
//                 }

//                 const data = await response.json();
//                 setProduct(data);
//             } catch (err) {
//                 console.error('Error fetching product:', err);
//                 setError(err.message);
//             } finally {
//                 setLoading(false);
//             }
//         };

//         fetchProductDetail();
//     }, [id]);

//     const handleGoBack = () => {
//         navigate(-1);
//     };

//     // 설명 데이터 파싱하는 함수
//     const parseProductDetails = (description) => {
//         if (!description) return [];

//         if (typeof description === 'object') {
//             return Object.entries(description)
//                 .filter(([key, value]) => value !== null && value !== "")
//                 .map(([key, value]) => ({
//                     label: key,
//                     value: typeof value === 'string' ? value : JSON.stringify(value)
//                 }));
//         }


//         try {
//             // JSON 형식인 경우
//             if (typeof description === 'string' &&
//                 (description.startsWith('{') || description.startsWith('['))) {
//                 const descObj = JSON.parse(description);

//                 // 객체인 경우
//                 if (descObj && typeof descObj === 'object' && !Array.isArray(descObj)) {
//                     return Object.entries(descObj)
//                         .filter(([key, value]) => value !== null && value !== '')
//                         .map(([key, value]) => ({
//                             label: key,
//                             value: typeof value === 'string' ? value : JSON.stringify(value)
//                         }));
//                 }
//             }

//             // 일반 문자열인 경우 - 줄바꿈으로 분리
//             return description.split('\n')
//                 .filter(line => line.trim())
//                 .map(line => {
//                     const parts = line.split(':');
//                     if (parts.length > 1) {
//                         return {
//                             label: parts[0].trim(),
//                             value: parts.slice(1).join(':').trim()
//                         };
//                     }
//                     return { label: '', value: line.trim() };
//                 });
//         } catch (e) {
//             console.error('Error parsing description:', e);
//             return [{ label: '', value: description }];
//         }
//     };

//     if (loading) {
//         return <div className="loading">로딩 중...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <p className="error-message">{error}</p>
//                 <button className="back-button" onClick={handleGoBack}>
//                     ⬅ 뒤로 가기
//                 </button>
//             </div>
//         );
//     }

//     // 상품 설명 파싱
//     const details = product?.description
//         ? parseProductDetails(product.description)
//         : [];

//     return (
//         <div className="product-detail-page">
//             <div className="product-container">
//                 {/* 첫 번째 섹션: 상품 갤러리 및 기본 정보 */}
//                 <div className="top-section">
//                     <div className="product-gallery">
//                         <div className="main-image">
//                             {product?.image_urls && product.image_urls.length > 0 ? (
//                                 <img
//                                     src={product.image_urls[selectedImage]}
//                                     alt={product.name}
//                                     className="featured-image"
//                                 />
//                             ) : (
//                                 <div className="no-image">이미지가 없습니다</div>
//                             )}
//                         </div>

//                         <div className="thumbnail-gallery">
//                             {product?.image_urls?.map((url, index) => (
//                                 <div
//                                     key={index}
//                                     className={`thumbnail ${selectedImage === index ? 'selected' : ''}`}
//                                     onClick={() => setSelectedImage(index)}
//                                 >
//                                     <img src={url} alt={`${product.name} - 이미지 ${index + 1}`} />
//                                 </div>
//                             ))}
//                         </div>
//                     </div>

//                     <div className="product-info">
//                         <h1 className="product-name">{product?.name}</h1>
//                         <p className="product-price">₩ {product?.price?.toLocaleString()}</p>

//                         <div className="product-actions">
//                             <a
//                                 href={product?.link}
//                                 target="_blank"
//                                 rel="noopener noreferrer"
//                                 className="buy-now-button"
//                             >
//                                 BUY NOW
//                             </a>
//                             <button className="add-to-cart-button">ADD TO CART</button>
//                         </div>
//                     </div>
//                 </div>

//                 {/* 두 번째 섹션: 상품 상세 정보 */}
//                 <div className="product-details">
//                     <h2>PRODUCT DETAILS</h2>
//                     <ul>
//                         {details.length > 0 ? (
//                             details.map((item, index) => (
//                                 <li key={index}>
//                                     {item.label && <strong>{item.label}</strong>}
//                                     {item.label && ': '}
//                                     {item.value}
//                                 </li>
//                             ))
//                         ) : (
//                             // 기본 정보 표시 (설명 데이터가 없을 경우)
//                             <>
//                                 <li>Material: 100% Cotton</li>
//                                 <li>Made in Korea</li>
//                                 <li>Care Instructions: Machine wash cold</li>
//                                 <li>Regular fit</li>
//                                 <li>Model is wearing size M</li>
//                             </>
//                         )}
//                     </ul>
//                 </div>

//                 <button className="back-button" onClick={handleGoBack}>
//                     ⬅ 검색 결과로 돌아가기
//                 </button>
//             </div>
//         </div>
//     );
// };

// export default ProductDetailPage;


// import { useEffect, useState } from 'react';
// import { useNavigate, useParams } from 'react-router-dom';
// import './ProductDetailPage.css';

// const ProductDetailPage = () => {
//     const { id } = useParams();
//     const [product, setProduct] = useState(null);
//     const [loading, setLoading] = useState(true);
//     const [error, setError] = useState(null);
//     const [selectedImage, setSelectedImage] = useState(0);
//     const navigate = useNavigate();

//     useEffect(() => {
//         const fetchProductDetail = async () => {
//             try {
//                 const response = await fetch(`/api/product/${id}`);

//                 if (!response.ok) {
//                     throw new Error('상품을 찾을 수 없습니다.');
//                 }

//                 const data = await response.json();
//                 setProduct(data);
//             } catch (err) {
//                 console.error('Error fetching product:', err);
//                 setError(err.message);
//             } finally {
//                 setLoading(false);
//             }
//         };

//         fetchProductDetail();
//     }, [id]);

//     const handleGoBack = () => {
//         navigate(-1);
//     };

//     // 설명 데이터 파싱하는 함수
//     const parseProductDetails = (description) => {
//         if (!description) return [];

//         if (typeof description === 'object') {
//             return Object.entries(description)
//                 .filter(([key, value]) => value !== null && value !== "")
//                 .map(([key, value]) => ({
//                     label: key,
//                     value: typeof value === 'string' ? value : JSON.stringify(value)
//                 }));
//         }

//         try {
//             // JSON 형식인 경우
//             if (typeof description === 'string' &&
//                 (description.startsWith('{') || description.startsWith('['))) {
//                 const descObj = JSON.parse(description);

//                 // 객체인 경우
//                 if (descObj && typeof descObj === 'object' && !Array.isArray(descObj)) {
//                     return Object.entries(descObj)
//                         .filter(([key, value]) => value !== null && value !== '')
//                         .map(([key, value]) => ({
//                             label: key,
//                             value: typeof value === 'string' ? value : JSON.stringify(value)
//                         }));
//                 }
//             }

//             // 일반 문자열인 경우 - 줄바꿈으로 분리
//             return description.split('\n')
//                 .filter(line => line.trim())
//                 .map(line => {
//                     const parts = line.split(':');
//                     if (parts.length > 1) {
//                         return {
//                             label: parts[0].trim(),
//                             value: parts.slice(1).join(':').trim()
//                         };
//                     }
//                     return { label: '', value: line.trim() };
//                 });
//         } catch (e) {
//             console.error('Error parsing description:', e);
//             return [{ label: '', value: description }];
//         }
//     };

//     if (loading) {
//         return <div className="loading">로딩 중...</div>;
//     }

//     if (error) {
//         return (
//             <div className="error-container">
//                 <p className="error-message">{error}</p>
//                 <button className="back-button" onClick={handleGoBack}>
//                     ⬅ 뒤로 가기
//                 </button>
//             </div>
//         );
//     }

//     // 상품 설명 파싱
//     const details = product?.description
//         ? parseProductDetails(product.description)
//         : [];

//     return (
//         <div className="product-detail-page">
//             <div className="product-container">
//                 {/* 상단 부분: 갤러리 섹션 */}
//                 <div className="gallery-section">
//                     <div className="thumbnail-gallery">
//                         {product?.image_urls?.map((url, index) => (
//                             <div
//                                 key={index}
//                                 className={`thumbnail ${selectedImage === index ? 'selected' : ''}`}
//                                 onClick={() => setSelectedImage(index)}
//                             >
//                                 <img src={url} alt={`${product.name} - 이미지 ${index + 1}`} />
//                             </div>
//                         ))}
//                     </div>

//                     <div className="main-image">
//                         {product?.image_urls && product.image_urls.length > 0 ? (
//                             <img
//                                 src={product.image_urls[selectedImage]}
//                                 alt={product.name}
//                                 className="featured-image"
//                             />
//                         ) : (
//                             <div className="no-image">이미지가 없습니다</div>
//                         )}
//                     </div>
//                 </div>

//                 {/* 중간 부분: 상품 정보 */}
//                 <div className="product-info">
//                     <h1 className="product-name">{product?.name}</h1>
//                     <p className="product-price">₩ {product?.price?.toLocaleString()}</p>

//                     <div className="product-actions">
//                         <a
//                             href={product?.link}
//                             target="_blank"
//                             rel="noopener noreferrer"
//                             className="buy-now-button"
//                         >
//                             BUY NOW
//                         </a>
//                         <button className="add-to-cart-button">ADD TO CART</button>
//                     </div>
//                 </div>

//                 {/* 하단 부분: 상품 상세 정보 */}
//                 <div className="product-details">
//                     <h2>PRODUCT DETAILS</h2>
//                     <ul>
//                         {details.length > 0 ? (
//                             details.map((item, index) => (
//                                 <li key={index}>
//                                     {item.label && <strong>{item.label}</strong>}
//                                     {item.label && ': '}
//                                     {item.value}
//                                 </li>
//                             ))
//                         ) : (
//                             // 기본 정보 표시 (설명 데이터가 없을 경우)
//                             <>
//                                 <li>Material: 100% Cotton</li>
//                                 <li>Made in Korea</li>
//                                 <li>Care Instructions: Machine wash cold</li>
//                                 <li>Regular fit</li>
//                                 <li>Model is wearing size M</li>
//                             </>
//                         )}
//                     </ul>
//                 </div>

//                 <button className="back-button" onClick={handleGoBack}>
//                     ⬅ 검색 결과로 돌아가기
//                 </button>
//             </div>
//         </div>
//     );
// };

// export default ProductDetailPage;



import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import './ProductDetailPage.css';

const ProductDetailPage = () => {
    const { id } = useParams();
    const [product, setProduct] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedImage, setSelectedImage] = useState(0);
    const navigate = useNavigate();

    useEffect(() => {
        const fetchProductDetail = async () => {
            try {
                const response = await fetch(`/api/product/${id}`);

                if (!response.ok) {
                    throw new Error('상품을 찾을 수 없습니다.');
                }

                const data = await response.json();
                setProduct(data);
            } catch (err) {
                console.error('Error fetching product:', err);
                setError(err.message);
            } finally {
                setLoading(false);
            }
        };

        fetchProductDetail();
    }, [id]);

    const handleGoBack = () => {
        navigate(-1);
    };

    // 설명 데이터 파싱하는 함수
    const parseProductDetails = (description) => {
        if (!description) return [];

        if (typeof description === 'object') {
            return Object.entries(description)
                .filter(([key, value]) => value !== null && value !== "")
                .map(([key, value]) => ({
                    label: key,
                    value: typeof value === 'string' ? value : JSON.stringify(value)
                }));
        }

        try {
            // JSON 형식인 경우
            if (typeof description === 'string' &&
                (description.startsWith('{') || description.startsWith('['))) {
                const descObj = JSON.parse(description);

                // 객체인 경우
                if (descObj && typeof descObj === 'object' && !Array.isArray(descObj)) {
                    return Object.entries(descObj)
                        .filter(([key, value]) => value !== null && value !== '')
                        .map(([key, value]) => ({
                            label: key,
                            value: typeof value === 'string' ? value : JSON.stringify(value)
                        }));
                }
            }

            // 일반 문자열인 경우 - 줄바꿈으로 분리
            return description.split('\n')
                .filter(line => line.trim())
                .map(line => {
                    const parts = line.split(':');
                    if (parts.length > 1) {
                        return {
                            label: parts[0].trim(),
                            value: parts.slice(1).join(':').trim()
                        };
                    }
                    return { label: '', value: line.trim() };
                });
        } catch (e) {
            console.error('Error parsing description:', e);
            return [{ label: '', value: description }];
        }
    };

    if (loading) {
        return <div className="loading">로딩 중...</div>;
    }

    if (error) {
        return (
            <div className="error-container">
                <p className="error-message">{error}</p>
                <button className="back-button" onClick={handleGoBack}>
                    ⬅ 뒤로 가기
                </button>
            </div>
        );
    }

    // 상품 설명 파싱
    const details = product?.description
        ? parseProductDetails(product.description)
        : [];

    // 브랜드 정보 (API에서 받아온 상품 데이터에 brand가 있다고 가정)
    // 실제 구현 시 API 응답에 맞게 조정 필요
    const brandName = product?.brand || "BRAND NAME"; // 기본값 제공

    return (
        <div className="product-detail-page">
            <div className="product-container">
                {/* 상단 부분: 갤러리 섹션 */}
                <div className="gallery-section">
                    <div className="thumbnail-gallery">
                        {product?.image_urls?.map((url, index) => (
                            <div
                                key={index}
                                className={`thumbnail ${selectedImage === index ? 'selected' : ''}`}
                                onClick={() => setSelectedImage(index)}
                            >
                                <img src={url} alt={`${product.name} - 이미지 ${index + 1}`} />
                            </div>
                        ))}
                    </div>

                    <div className="main-image">
                        {product?.image_urls && product.image_urls.length > 0 ? (
                            <img
                                src={product.image_urls[selectedImage]}
                                alt={product.name}
                                className="featured-image"
                            />
                        ) : (
                            <div className="no-image">이미지가 없습니다</div>
                        )}
                    </div>
                </div>

                {/* 중간 부분: 상품 정보 */}
                <div className="product-info">
                    <div className="brand-name">{brandName}</div>
                    <h1 className="product-name">{product?.name}</h1>
                    <p className="product-price">₩ {product?.price?.toLocaleString()}</p>

                    <div className="product-actions">
                        <a
                            href={product?.link}
                            target="_blank"
                            rel="noopener noreferrer"
                            className="buy-now-button"
                        >
                            BUY NOW
                        </a>
                        <button className="add-to-cart-button">ADD TO CART</button>
                    </div>
                </div>

                {/* 하단 부분: 상품 상세 정보 */}
                <div className="product-details">
                    <h2>PRODUCT DETAILS</h2>
                    <ul>
                        {details.length > 0 ? (
                            details.map((item, index) => (
                                <li key={index}>
                                    {item.label && <strong>{item.label}</strong>}
                                    {item.label && ': '}
                                    {item.value}
                                </li>
                            ))
                        ) : (
                            // 기본 정보 표시 (설명 데이터가 없을 경우)
                            <>
                                <li>Material: 100% Cotton</li>
                                <li>Made in Korea</li>
                                <li>Care Instructions: Machine wash cold</li>
                                <li>Regular fit</li>
                                <li>Model is wearing size M</li>
                            </>
                        )}
                    </ul>
                </div>

                <button className="back-button" onClick={handleGoBack}>
                    ⬅ 검색 결과로 돌아가기
                </button>
            </div>
        </div>
    );
};

export default ProductDetailPage;