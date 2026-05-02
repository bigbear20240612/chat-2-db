// TODO  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82YUhoc1pBPT06Y2ZjYWY3NWQ=

const reportWebVitals = (onPerfEntry) => {
  if (onPerfEntry && onPerfEntry instanceof Function) {
    import('web-vitals').then(({ getCLS, getFID, getFCP, getLCP, getTTFB }) => {
      getCLS(onPerfEntry);
      getFID(onPerfEntry);
      getFCP(onPerfEntry);
      getLCP(onPerfEntry);
      getTTFB(onPerfEntry);
    });
  }
};
// FIXME  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82YUhoc1pBPT06Y2ZjYWY3NWQ=

export default reportWebVitals;
