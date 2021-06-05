docker build -t nuuuwan/gig_server .
echo 'Docker build complete. Starting server...'
docker run -p 4001:4001 nuuuwan/gig_server
